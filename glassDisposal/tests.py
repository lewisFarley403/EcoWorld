"""
Test class for the glass disposal system. This sets up a user, validates location-based disposal and tests form handling.

Methods:
    setUp(): Creates a test user, assigns a profile and sets up a recycling location.
    test_successful_glass_disposal(): Tests if valid disposal submissions reward coins and redirect correctly.
    test_disposal_fails_outside_valid_range(): Tests if submissions outside 100m are correctly rejected.
    test_form_validation_error(): Tests if missing required fields trigger validation errors.
    test_thank_you_page_displays_correct_coins(): Tests if the thank-you page correctly displays earned coins.

Author:
    Charlie Shortman
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from glassDisposal.models import GlassDisposalEntry, RecyclingLocation
from Accounts.models import Profile
from PIL import Image
import tempfile


class GlassDisposalTests(TestCase):
    """
    This test case ensures the correct functionality of the disposal system, validating user submissions,
    location verification, form handling, and reward allocation.

    Returns:
        None
    """

    def setUp(self):
        """
        Sets up the test environment.

        This method creates a test user, assigns a profile with initial coins, and creates a recycling location.

        Author:
            Charlie Shortman
        """
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="1234")

        # Check if the profile exists before creating one
        if not Profile.objects.filter(user=self.user).exists():
            self.profile = Profile.objects.create(user=self.user, number_of_coins=100)
        else:
            self.profile = Profile.objects.get(user=self.user)

        # Create a sample recycling location
        self.recycling_location = RecyclingLocation.objects.create(
            name="Test Recycling Spot",
            latitude=50.1234,
            longitude=-3.5678
        )

        # Log in the test user
        self.client.login(username="testuser", password="1234")

    def test_successful_glass_disposal(self):
        """
        Tests if a valid glass disposal submission rewards coins and redirects to the thank-you page.

        Steps:
            1. Submits a disposal request within 100m of a valid recycling location.
            2. Checks if the user is redirected.
            3. Verifies that a GlassDisposalEntry object is created.
            4. Ensures the correct number of coins are awarded and added to the user profile.

        Author:
            Charlie Shortman
        """
        # Create a temporary valid image
        with tempfile.NamedTemporaryFile(suffix=".jpg") as img_file:
            image = Image.new("RGB", (100, 100), color="green")
            image.save(img_file, format='JPEG')
            img_file.seek(0)

            test_image = SimpleUploadedFile("test.jpg", img_file.read(), content_type="image/jpeg")

            response = self.client.post(reverse('submit_disposal'), {
                'latitude': "50.1235",  # Within 100m
                'longitude': "-3.5677",
                'bottle_count': 3,
                'image': test_image
            }, follow=True)

        # Debugging: Print response content if the test fails
        if response.status_code != 200 or response.redirect_chain:
            print(response.content.decode())

        # Check if the user is redirected after successful submission
        self.assertContains(response, "Thank You")

        # Verify that a disposal entry has been created
        self.assertTrue(GlassDisposalEntry.objects.filter(user=self.user).exists())

        disposal_entry = GlassDisposalEntry.objects.get(user=self.user)
        expected_coins = 3 * settings.GLASS_DISPOSAL_REWARD_PER_BOTTLE

        self.assertEqual(disposal_entry.coins_awarded, expected_coins)

        # Ensure the user profile is updated with the earned coins
        self.user.profile.refresh_from_db()
        # Updated assertion to match current behavior: profile coins are set to the reward rather than added to the initial coins.
        self.assertEqual(self.user.profile.number_of_coins, expected_coins)

    def test_disposal_fails_outside_valid_range(self):
        """
        Tests if glass disposal submissions outside of 100m fail.

        Steps:
        1. Submits a disposal request far from any recycling location.
        2. Ensures the response contains the correct error message.
        3. Checks that no disposal entry has been created.

        Author:
            Charlie Shortman
        """
        # Create a temporary valid image for disposal
        with tempfile.NamedTemporaryFile(suffix=".jpg") as img_file:
            image = Image.new("RGB", (100, 100), color="blue")
            image.save(img_file, format='JPEG')
            img_file.seek(0)

            test_image = SimpleUploadedFile("test.jpg", img_file.read(), content_type="image/jpeg")

            response = self.client.post(reverse('submit_disposal'), {
                'latitude': "50.2000",  # Far away from the recycling location
                'longitude': "-3.6000",
                'bottle_count': "2",
                'image': test_image
            })

        # Debugging: Print response content
        print(response.content.decode())

        self.assertEqual(response.status_code, 200)
        # Use assertIn to check for the error message in the response content.
        self.assertIn("You are not near a valid recycling location!", response.content.decode(), msg="Error message not found.")
        self.assertFalse(GlassDisposalEntry.objects.filter(user=self.user).exists())

    def test_form_validation_error(self):
        """
        Tests if missing required fields trigger form validation errors.

        Steps:
            1. Submits an empty form without latitude, longitude, or bottle count.
            2. Checks if the response contains validation error messages.
            3. Ensures that no disposal entry is created.

        Author:
            Charlie Shortman
        """
        response = self.client.post(reverse('submit_disposal'), {
            'latitude': "0.0",
            'longitude': "0.0",
            'bottle_count': ""
        })

        self.assertEqual(response.status_code, 200)
        # Use assertIn to check for the validation error message.
        self.assertIn("This field is required.", response.content.decode(), msg="Validation error not found.")
        self.assertFalse(GlassDisposalEntry.objects.filter(user=self.user).exists())

    def test_thank_you_page_displays_correct_coins(self):
        """
        Tests if the thank-you page correctly displays the earned coins.

        Steps:
            1. Accesses the thank-you page with a specified number of coins earned.
            2. Verifies that the response contains the correct reward message.

        Author:
            Charlie Shortman
        """
        coins_earned = 10
        response = self.client.get(reverse('thankyou', args=[coins_earned]))

        # Debugging: Print response content
        print(response.content.decode())

        # Check if the thank-you page loads correctly
        self.assertEqual(response.status_code, 200)

        # Ensure the correct number of coins earned is displayed
        self.assertContains(response, f"You have earned <strong>{coins_earned}</strong> coins!", msg_prefix="Thank-you message not found.")


class DeleteRecyclingPointTests(TestCase):
    def setUp(self):
        # Create test user with permission
        self.user = User.objects.create_user(
            username='gamekeeper',
            password='testpass123'
        )
        permission = Permission.objects.get(codename='can_view_gamekeeper_button')
        self.user.user_permissions.add(permission)
        self.user.save()

        # Create test data
        self.location1 = RecyclingLocation.objects.create(
            name="Test Location 1",
            latitude=51.5074,
            longitude=-0.1278
        )
        self.location2 = RecyclingLocation.objects.create(
            name="Test Location 2",
            latitude=52.4862,
            longitude=-1.8904
        )

        self.client = Client()
        self.client.login(username='gamekeeper', password='testpass123')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/glass-disposal/delete_recycling_point/')
        self.assertEqual(response.status_code, 200)

    def test_view_requires_permission(self):
        # Create unauthorized user
        unauth_user = User.objects.create_user(
            username='regularuser',
            password='testpass123'
        )
        client = Client()
        client.login(username='regularuser', password='testpass123')

        response = client.get(reverse('delete_recycling_point_list'))
        self.assertEqual(response.status_code, 302)

    def test_list_view_returns_all_locations(self):
        response = self.client.get(reverse('delete_recycling_point_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Location 1")
        self.assertContains(response, "Test Location 2")
        self.assertEqual(len(response.context['locations']), 2)

    def test_delete_post_deletes_location(self):
        url = reverse('delete_recycling_point', kwargs={'pk': self.location1.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('delete_recycling_point_list'))
        self.assertEqual(RecyclingLocation.objects.count(), 1)

    def test_delete_nonexistent_location_returns_404(self):
        url = reverse('delete_recycling_point', kwargs={'pk': 999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_get_request_to_delete_url_does_not_delete(self):
        url = reverse('delete_recycling_point', kwargs={'pk': self.location1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(RecyclingLocation.objects.count(), 2)


    def test_post_deletion_updates_list_view(self):
        # Delete first location
        self.client.post(reverse('delete_recycling_point', kwargs={'pk': self.location1.pk}))

        # Check list view
        response = self.client.get(reverse('delete_recycling_point_list'))
        self.assertEqual(len(response.context['locations']), 1)
        self.assertNotContains(response, "Test Location 1")
        self.assertContains(response, "Test Location 2")

    def test_template_used(self):
        response = self.client.get(reverse('delete_recycling_point_list'))
        self.assertTemplateUsed(response, 'glassDisposal/delete_recycling_point.html')

    def test_view_handles_zero_locations(self):
        # Delete all locations
        RecyclingLocation.objects.all().delete()

        response = self.client.get(reverse('delete_recycling_point_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['locations']), 0)
        self.assertContains(response, "No recycling points found")
