from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission

from EcoWorld.forms import ChallengeForm
from EcoWorld.models import challenge
from qrCodes.models import drinkEvent, waterFountain
import json

class GamekeeperViewTests(TestCase):
    def setUp(self):
        # Create a gamekeeper user and a regular user.
        self.gamekeeper_user = User.objects.create_user(username="gamekeeper", password="gamekeeperpassword")
        self.regular_user = User.objects.create_user(username="user", password="userpassword")

        # Get and assign the permission to view gamekeeper pages.
        self.gamekeeper_permission = Permission.objects.get(codename="can_view_gamekeeper_button")
        self.gamekeeper_user.user_permissions.add(self.gamekeeper_permission)

    # --- Tests for the gamekeeper_page view ---

    def test_gamekeeper_page_access_as_gamekeeper(self):
        """An authorized gamekeeper user should see the gamekeeper page."""
        self.client.login(username="gamekeeper", password="gamekeeperpassword")
        response = self.client.get(reverse("EcoWorld:gamekeeper_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "EcoWorld/gamekeeper_page.html")
        # Check that expected context data is present.
        self.assertIn("userinfo", response.context)
        self.assertIn("users", response.context)
        self.assertIn("missing_rows", response.context)

    def test_gamekeeper_page_access_as_regular_user(self):
        """A regular user should be redirected (unauthorized) when accessing the gamekeeper page."""
        self.client.login(username="user", password="userpassword")
        response = self.client.get(reverse("EcoWorld:gamekeeper_page"))
        # Expecting a 302 redirect to the login page.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/?next=/ecoworld/gamekeeper/"))

    def test_gamekeeper_page_access_unauthenticated(self):
        """An unauthenticated request should redirect to the login page."""
        response = self.client.get(reverse("EcoWorld:gamekeeper_page"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/?next=/ecoworld/gamekeeper/"))

    # --- Tests for the grant_gamekeeper view ---

    def test_grant_gamekeeper_as_gamekeeper(self):
        """An gamekeeper can grant gamekeeper privileges to another user."""
        self.client.login(username="gamekeeper", password="gamekeeperpassword")
        response = self.client.post(reverse("EcoWorld:grant_gamekeeper", args=[self.regular_user.id]))
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.has_perm("Accounts.can_view_gamekeeper_button"))
        self.assertRedirects(response, reverse("EcoWorld:gamekeeper_page"))

    def test_grant_gamekeeper_as_regular_user(self):
        """A regular user should be redirected when attempting to grant gamekeeper privileges."""
        self.client.login(username="user", password="userpassword")
        response = self.client.post(reverse("EcoWorld:grant_gamekeeper", args=[self.gamekeeper_user.id]))
        # By default, @permission_required redirects unauthorized users to login.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/?next=/ecoworld/grant_gamekeeper/1/"))

    # --- Tests for the add_challenge view ---

    def test_add_challenge_as_gamekeeper(self):
        """An gamekeeper should be able to add a new challenge."""
        self.client.login(username="gamekeeper", password="gamekeeperpassword")
        post_data = {
            "name": "New Challenge",
            "description": "Test challenge",
            "worth": 10,
            "goal": 5,
        }
        response = self.client.post(reverse("EcoWorld:add_challenge"), post_data)
        # On successful submission, the view redirects to the gamekeeper page.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("EcoWorld:gamekeeper_page"))
        # Verify that the challenge was created.
        self.assertEqual(challenge.objects.count(), 1)

    def test_add_challenge_as_regular_user(self):
        """A regular user should be redirected when trying to add a challenge."""
        self.client.login(username="user", password="userpassword")
        post_data = {
            "name": "New Challenge",
            "description": "Test challenge",
            "worth": 10,
            "goal": 5,
        }
        response = self.client.post(reverse("EcoWorld:add_challenge"), post_data)
        # Unauthorized users are redirected to login.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/?next=/ecoworld/add-challenge/"))
        # No new challenge should be created.
        self.assertEqual(challenge.objects.count(), 0)

    def test_add_challenge_form_display(self):
        """The challenge form should be displayed for an gamekeeper accessing the page via GET."""
        self.client.login(username="gamekeeper", password="gamekeeperpassword")
        response = self.client.get(reverse("EcoWorld:add_challenge"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], ChallengeForm)
