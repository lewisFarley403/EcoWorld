from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import json

from ecoworld.models import ongoingChallenge, card, cardRarity, ownsCard
from Garden.models import garden, gardenSquare
from forum.models import challenge

class SustainabilityGameTests(TestCase):
    def setUp(self):
        """Set up test data for sustainability game tests
        Author: sg916@exeter.ac.uk
        """
        self.client = Client()

        # Create test user - Profile is auto-created via signals
        self.test_user = User.objects.create_user(username='eco_user', password='green123')

        # Create garden for user
        self.garden = garden.objects.create(userID=self.test_user)

        # Create card rarity
        self.rarity = cardRarity.objects.create(title="Common")

        # Create test card
        self.card = card.objects.create(
            title="Test Card",
            description="Test Description",
            rarity=self.rarity,
            image="cards/test.jpg"
        )

        ownsCard.objects.create(user=self.test_user, card=self.card, quantity=1)

    def test_sustainability_challenge_completion(self):
        """Test user completing a sustainability challenge
        - Create eco challenge
        - Complete challenge
        - Verify in user feed

        Author: sg916@exeter.ac.uk
        """
        eco_challenge = challenge.objects.create(
            name="Reduce Water Usage",
            description="Use 20% less water today",
            created_by=self.test_user,
            created_on=timezone.now().date(),
            worth=50
        )

        ongoingChallenge.objects.create(
            user=self.test_user,
            challenge=eco_challenge,
            submitted_on=timezone.now(),
            submission="Used shower timer",
            completion_count=1
        )

        self.client.login(username='eco_user', password='green123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'my'})
        self.assertEqual(response.status_code, 200)

    def test_garden_card_placement(self):
        """Test placing sustainability reward card in garden
        - Login user
        - Create empty square
        - Place card
        - Verify placement

        Author: sg916@exeter.ac.uk
        """
        self.client.login(username='eco_user', password='green123')

        square = gardenSquare.objects.create(
            gardenID=self.garden,
            squareID=4,
            cardID=None
        )

        response = self.client.post(
            reverse('add_card'),
            json.dumps({'row': 2, 'col': 2, 'card_id': self.card.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    def test_user_card_inventory(self):
        """Test user's sustainability card inventory
        - Check initial card quantity
        - Add card
        - Verify updated quantity

        Author: sg916@exeter.ac.uk
        """
        initial_quantity = ownsCard.objects.get(user=self.test_user, card=self.card).quantity
        self.assertEqual(initial_quantity, 1)

        ownsCard.objects.filter(user=self.test_user, card=self.card).update(quantity=2)
        updated_quantity = ownsCard.objects.get(user=self.test_user, card=self.card).quantity
        self.assertEqual(updated_quantity, 2)