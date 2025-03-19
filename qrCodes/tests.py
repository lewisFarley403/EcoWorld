from datetime import timedelta

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
        # Create an admin user and a regular user.
        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.regular_user = User.objects.create_user(username='user', password='userpass')

        # Give the admin user the required permission.
        permission = Permission.objects.get(codename="can_view_admin_button")
        self.admin_user.user_permissions.add(permission)

        # Use get_or_create so that if a Profile is already auto-created, we simply retrieve it.
        self.admin_profile, _ = Profile.objects.get_or_create(user=self.admin_user, defaults={'number_of_coins': 0})
        self.regular_profile, _ = Profile.objects.get_or_create(user=self.regular_user, defaults={'number_of_coins': 0})

        # Ensure the coin count is 0 at the start.
        self.admin_profile.number_of_coins = 0
        self.admin_profile.save()
        self.regular_profile.number_of_coins = 0
        self.regular_profile.save()

        # Create a water fountain instance for tests.
        self.fountain = waterFountain.objects.create(name="Test Fountain")

    # --- Tests for generate_qr_code view ---
    def test_generate_qr_code_access_by_admin(self):
        """A user with the proper permission should access the QR generation page."""
        self.client.login(username='admin', password='adminpass')
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
        past_time = timezone.now() - (settings.DRINKING_COOLDOWN + timedelta(minutes=1))
        drinkEvent.objects.create(user=self.regular_user, fountain=self.fountain, drank_on=past_time)
        initial_coins = self.regular_user.profile.number_of_coins

        url = reverse('qrCodes:scan_qr')
        response = self.client.get(url, {'id': self.fountain.id})
        # Expecting the view to render 'drink_registered.html'
        self.assertTemplateUsed(response, 'drink_registered.html')
        self.assertEqual(drinkEvent.objects.filter(user=self.regular_user).count(), 2)

        self.regular_user.profile.refresh_from_db()
        expected_coins = initial_coins + settings.VALUE_OF_DRINK
        self.assertEqual(self.regular_user.profile.number_of_coins, expected_coins)

    # --- Tests for add_water_fountain view ---
    def test_add_water_fountain_get(self):
        """An admin should see the water fountain form when accessing the page via GET."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('qrCodes:add_water_fountain'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_water_fountain.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], WaterFountainForm)

    def test_add_water_fountain_post_valid(self):
        """
        A valid POST by an admin should create a new waterFountain and redirect.
        Note: The view redirects to "EcoWorld:admin_page". Adjust this if your redirect URL changes.
        """
        self.client.login(username='admin', password='adminpass')
        # IMPORTANT: Update post_data with all required fields for WaterFountainForm.
        post_data = {
            'name': 'New Fountain',
            # e.g., 'description': 'Test fountain description', 'location': 'Test location'
        }
        response = self.client.post(reverse('qrCodes:add_water_fountain'), post_data)
        # Check if the form validated and the view redirected.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('EcoWorld:admin_page'))
        self.assertEqual(waterFountain.objects.filter(name='New Fountain').count(), 1)

    def test_add_water_fountain_post_invalid(self):
        """
        An invalid POST (e.g. missing required fields) should re-render the form with errors.
        """
        self.client.login(username='admin', password='adminpass')
        post_data = {
            'name': '',  # Assuming an empty name is invalid.
        }
        response = self.client.post(reverse('qrCodes:add_water_fountain'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_water_fountain.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_add_water_fountain_access_regular_user(self):
        """A non-admin user should be redirected when trying to access the add water fountain view."""
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('qrCodes:add_water_fountain'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
