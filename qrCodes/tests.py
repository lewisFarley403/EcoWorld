import datetime
from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from django.conf import settings

from qrCodes.models import waterFountain, drinkEvent
from qrCodes.forms import WaterFountainForm

# Import your actual Profile model from the Accounts app
from Accounts.models import Profile


class QRCodesViewsTests(TestCase):
    def setUp(self):
        # Create an gamekeeper user and a regular user.
        self.gamekeeper_user = User.objects.create_user(username='gamekeeper', password='gamekeeperpass')
        self.regular_user = User.objects.create_user(username='user', password='userpass')

        # Give the gamekeeper user the required permission.
        permission = Permission.objects.get(codename="can_view_gamekeeper_button")
        self.gamekeeper_user.user_permissions.add(permission)

        # Use get_or_create so that if a Profile is already auto-created, we simply retrieve it.
        self.gamekeeper_profile, _ = Profile.objects.get_or_create(user=self.gamekeeper_user, defaults={'number_of_coins': 0})
        self.regular_profile, _ = Profile.objects.get_or_create(user=self.regular_user, defaults={'number_of_coins': 0})

        # Ensure the coin count is 0 at the start.
        self.gamekeeper_profile.number_of_coins = 0
        self.gamekeeper_profile.save()
        self.regular_profile.number_of_coins = 0
        self.regular_profile.save()

        # Create a water fountain instance for tests.
        self.fountain = waterFountain.objects.create(name="Test Fountain")

    # --- Tests for generate_qr_code view ---
    def test_generate_qr_code_access_by_gamekeeper(self):
        """A user with the proper permission should access the QR generation page."""
        self.client.login(username='gamekeeper', password='gamekeeperpass')
        response = self.client.get(reverse('qrCodes:generate_qr'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'make_qr_code.html')
        self.assertIn('fountains', response.context)
        self.assertIn('width', response.context)
        self.assertIn('height', response.context)

    def test_generate_qr_code_access_by_regular_user(self):
        """A regular user should be redirected when accessing the QR generation page."""
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('qrCodes:generate_qr'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_generate_qr_code_access_unauthenticated(self):
        """Unauthenticated users should be redirected to the login page."""
        response = self.client.get(reverse('qrCodes:generate_qr'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # --- Tests for scan_qr_page view (formerly scan_code_page) ---
    def test_scan_qr_page_requires_login(self):
        """The scan QR page should only be accessible to logged-in users."""
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('qrCodes:scan_qr_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qr_scanner.html')

    def test_scan_qr_page_redirects_if_not_logged_in(self):
        """Unauthenticated users should be redirected when accessing the scanner page."""
        response = self.client.get(reverse('qrCodes:scan_qr_page'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    # --- Tests for scan_qr view (formerly scan_code) ---
    def test_scan_qr_no_previous_event(self):
        """
        When the user has no previous drink event, scanning a valid fountain code should:
          - Create a new drinkEvent.
          - Increase the user's coins by VALUE_OF_DRINK.
          - Render the 'drink_registered.html' template.
        """
        self.client.login(username='user', password='userpass')
        initial_coins = self.regular_user.profile.number_of_coins

        url = reverse('qrCodes:scan_qr')
        response = self.client.get(url, {'id': self.fountain.id})
        self.assertTemplateUsed(response, 'drink_registered.html')
        self.assertEqual(drinkEvent.objects.filter(user=self.regular_user).count(), 1)

        # Refresh profile from DB after view call.
        self.regular_user.profile.refresh_from_db()
        expected_coins = initial_coins + settings.VALUE_OF_DRINK
        self.assertEqual(self.regular_user.profile.number_of_coins, expected_coins)

    def test_scan_qr_within_cooldown(self):
        """
        If the user’s last drink event was within the DRINKING_COOLDOWN period,
        the view should render 'drink_cooldown_page.html' and not create a new event.
        """
        self.client.login(username='user', password='userpass')
        recent_time = timezone.now() - (settings.DRINKING_COOLDOWN / 2)
        drinkEvent.objects.create(user=self.regular_user, fountain=self.fountain, drank_on=recent_time)
        initial_coins = self.regular_user.profile.number_of_coins

        url = reverse('qrCodes:scan_qr')
        response = self.client.get(url, {'id': self.fountain.id})
        self.assertTemplateUsed(response, 'drink_cooldown_page.html')
        self.assertEqual(drinkEvent.objects.filter(user=self.regular_user).count(), 1)

        # Refresh profile and assert coins remain unchanged.
        self.regular_user.profile.refresh_from_db()
        self.assertEqual(self.regular_user.profile.number_of_coins, initial_coins)

    def test_scan_qr_after_cooldown(self):
        """
        If the user’s last drink event was longer ago than DRINKING_COOLDOWN,
        a new drink event should be created and coins updated.
        """
        self.client.login(username='user', password='userpass')

        # Mock timezone.now() to return a fixed time during the test
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = timezone.make_aware(datetime.datetime(2025, 3, 19, 13, 30, 0))

            # Set past_time to the previous day (24 hours before mock_now)
            past_time = mock_now.return_value - timedelta(days=1)

            # Create the previous drink event with past_time
            drinkEvent.objects.create(user=self.regular_user, fountain=self.fountain, drank_on=past_time)

            # Save initial coins for comparison
            initial_coins = self.regular_user.profile.number_of_coins

            # Send the GET request to scan the QR code
            url = reverse('qrCodes:scan_qr')
            response = self.client.get(url, {'id': self.fountain.id})

            # Verify that the correct template is used
            self.assertTemplateUsed(response, 'drink_registered.html')

            # Verify a new drink event was created
            self.assertEqual(drinkEvent.objects.filter(user=self.regular_user).count(), 2)

            # Verify that the user's coins have been updated
            self.regular_user.profile.refresh_from_db()
            expected_coins = initial_coins + settings.VALUE_OF_DRINK
            self.assertEqual(self.regular_user.profile.number_of_coins, expected_coins)


    # --- Tests for add_water_fountain view ---
    def test_add_water_fountain_get(self):
        """An gamekeeper should see the water fountain form when accessing the page via GET."""
        self.client.login(username='gamekeeper', password='gamekeeperpass')
        response = self.client.get(reverse('qrCodes:add_water_fountain'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_water_fountain.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], WaterFountainForm)

    def test_add_water_fountain_post_valid(self):
        """
        A valid POST by an gamekeeper should create a new waterFountain and redirect.
        """
        self.client.login(username='gamekeeper', password='gamekeeperpass')

        # Ensure all required fields are included
        post_data = {
            'name': 'New Fountain',
            'location': 'Test Location',  # Required field
        }

        response = self.client.post(reverse('qrCodes:add_water_fountain'), post_data)

        # Print form errors if the test still fails
        print(response.context.get('form').errors if response.context else "No form errors")

        # Check if the form validated and the view redirected.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('EcoWorld:gamekeeper_page'))
        self.assertEqual(waterFountain.objects.filter(name='New Fountain').count(), 1)


    def test_add_water_fountain_post_invalid(self):
        """
        An invalid POST (e.g. missing required fields) should re-render the form with errors.
        """
        self.client.login(username='gamekeeper', password='gamekeeperpass')
        post_data = {
            'name': '',  # Assuming an empty name is invalid.
        }
        response = self.client.post(reverse('qrCodes:add_water_fountain'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_water_fountain.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_add_water_fountain_access_regular_user(self):
        """A non-gamekeeper user should be redirected when trying to access the add water fountain view."""
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('qrCodes:add_water_fountain'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
