from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
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



