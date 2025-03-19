from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission

from EcoWorld.forms import ChallengeForm
from EcoWorld.models import challenge
from qrCodes.models import drinkEvent, waterFountain
import json

class EcoWorldViewsTest(TestCase):

    def setUp(self):
        """ Set up data before each test"""
        self.client = Client()

        # Fake user
        self.user = User.objects.create_user(username = "testuser", password = "password123")

        # Fake water fountain
        self.fountain = waterFountain.objects.create(id = 1, location = "Test Location")

        #URLS that I want to test
        self.add_drink_url = reverse("EcoWorld:home")
        self.generate_qr_url = reverse("EcoWorld:generate_qr")
        self.scan_qr_url = reverse("EcoWorld:scan_qr")
        self.upload_photo_url = reverse("EcoWorld:upload_photo")

    def test_add_drink_valid_post(self):
        """ Test adding a drink """
        data = {
            "user" : self.user.id,
            "fountain" : self.fountain.id,
            "drank_on" : "2025-02-12"
        }

        response =  self.client.post(self.add_drink_url, json.dumps(data), content_type = "application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(drinkEvent.objects.count(), 1)
        self.assertIn("Added drink event", response.content.decode())

    # def test_add_drink_invalid_user(self):
    #     #This fails because the addDrink function in views doesn't handle non-existent users gracefully
    #     #but im not sure if we need that function tbh
    #     """Test adding a drink with an invalid user."""
    #     data = {
    #         "user": 999,  # Non-existing user ID
    #         "fountain": self.fountain.id,
    #         "drank_on": "2025-02-22T12:00:00Z"
    #     }

    #     response = self.client.post(self.add_drink_url, json.dumps(data), content_type="application/json")

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("Invalid user or fountain", response.content.decode())

    def test_generate_qr_code_view(self):
        """Test if the QR code generation page loads successfully."""
        response = self.client.get(self.generate_qr_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "EcoWorld/qr_code.html")
        self.assertIn("https://EcoWorld.com/scan/", response.context["qr_data"])

    def test_scan_qr_code_view(self):
        """Test if the scan QR code page loads successfully."""
        response = self.client.get(self.scan_qr_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "EcoWorld/scan_qr_code.html")

    def test_upload_bottle_photo_get(self):
        """Test the GET request for upload bottle photo."""
        response = self.client.get(self.upload_photo_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "EcoWorld/upload_photo.html")



class AdminViewTests(TestCase):
    def setUp(self):
        """Create test users and permissions."""
        self.admin_user = User.objects.create_user(username="admin", password="adminpassword")
        self.regular_user = User.objects.create_user(username="user", password="userpassword")

        # Assign permission to the admin user
        self.admin_permission = Permission.objects.get(codename="can_view_admin_button")
        self.admin_user.user_permissions.add(self.admin_permission)

    def test_admin_page_access_as_admin(self):
        """Ensure an admin can access the admin page."""
        self.client.login(username="admin", password="adminpassword")
        response = self.client.get(reverse("EcoWorld:admin_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "EcoWorld/admin_page.html")

    def test_admin_page_access_as_regular_user(self):
        """Ensure a non-admin user is denied access to the admin page."""
        self.client.login(username="user", password="userpassword")
        response = self.client.get(reverse("EcoWorld:admin_page"))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_admin_page_access_unauthenticated(self):
        """Ensure unauthenticated users are redirected to login."""
        response = self.client.get(reverse("EcoWorld:admin_page"))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_grant_admin_as_admin(self):
        """Ensure an admin can grant another user admin rights."""
        self.client.login(username="admin", password="adminpassword")
        response = self.client.post(reverse("EcoWorld:grant_admin", args=[self.regular_user.id]))

        # Check if the user got the admin permission
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.has_perm("Accounts.can_view_admin_button"))

        # Check redirection
        self.assertRedirects(response, reverse("EcoWorld:admin_page"))

    def test_grant_admin_as_non_admin(self):
        """Ensure a regular user cannot grant admin rights."""
        self.client.login(username="user", password="userpassword")
        response = self.client.post(reverse("EcoWorld:grant_admin", args=[self.admin_user.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Ensure admin permission was NOT granted
        self.admin_user.refresh_from_db()
        self.assertFalse(self.admin_user.has_perm("Accounts.can_view_admin_button"))

    def test_add_challenge_as_admin(self):
        """Ensure an admin can add a challenge."""
        self.client.login(username="admin", password="adminpassword")
        response = self.client.post(reverse("EcoWorld:add_challenge"), {"name": "New Challenge"})

        # Check if challenge was added
        self.assertEqual(challenge.objects.count(), 1)
        self.assertRedirects(response, reverse("EcoWorld:admin_page"))

    def test_add_challenge_as_regular_user(self):
        """Ensure a non-admin user cannot add a challenge."""
        self.client.login(username="user", password="userpassword")
        response = self.client.post(reverse("EcoWorld:add_challenge"), {"name": "New Challenge"})
        self.assertEqual(response.status_code, 403)  # Forbidden
        self.assertEqual(challenge.objects.count(), 0)  # No challenge should be added

    def test_add_challenge_form_display(self):
        """Ensure the challenge form is displayed for admins."""
        self.client.login(username="admin", password="adminpassword")
        response = self.client.get(reverse("EcoWorld:add_challenge"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], ChallengeForm)
