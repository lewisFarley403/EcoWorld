"""
Test class for the garden app. This sets up a garden with users and then checks what happenes when adding and removing owned cards in the garden
Methods:
    setUp(): This method sets up each user and their associated garden along with cards to be used in the other tests
    testGardenLogin() : Tests that the garden page requires login to work
    testGardenView() : Tests to make sure the garden works when loaded in
    testAddCardToGardenSuccess() : Checks that when dragging and dropping a card into garden it works
    testAddCardToGardenFailIfOccupied() : Checks that user cant add a card to an already occupied square
    testRemoveCardSuccess() : Tests that when removing a card it works and nothing breaks
    testRemoveCardFail() : Checks that if user tries to remove card from empty square it doesnt crash

Author:
Chris Lynch (cl1037@exeter.ac.uk)


"""
import json

from django.test import TestCase, Client
from django.urls import reverse

from Accounts.models import Profile
from ecoworld.models import cardRarity, ownsCard, card
from .models import garden, gardenSquare, User


class TestGarden(TestCase):

    def setUp(self):
        self.client = Client()

        #Create test user
        self.user1 = User.objects.create_user(username="testuser1", password="1234")

        #Create profile
        self.profile1, _ = Profile.objects.get_or_create(user=self.user1, 
                                                        defaults={"number_of_coins": 100,
                                                                "profile_picture": "pfp1.png"})

        #Create card raritys for the cards being used
        self.common_rarity, _ = cardRarity.objects.get_or_create(id=1, defaults={"title": "common"})
        self.rare_rarity, _ = cardRarity.objects.get_or_create(id=2, defaults={"title": "rare"})
        self.legendary_rarity, _ = cardRarity.objects.get_or_create(id=4,
                                                                    defaults={"title": "legendary"})

        #Give the cards their rarities so they dont crash when placed
        self.card1 = card.objects.create(title="Bush",
                                        image="cards/bush.png",
                                        rarity=self.common_rarity)
        self.card2 = card.objects.create(title="Cactus",
                                        image="cards/cactus.png",
                                        rarity=self.rare_rarity)
        self.card3 = card.objects.create(title="Cherry Blossom",
                                        image="cards/cherryBlossom.png",
                                        rarity=self.legendary_rarity)

        #Giving user 1 bush cards for placement
        self.owns_card1, _ = ownsCard.objects.get_or_create(user=self.user1,
                                                            card=self.card1,
                                                            defaults={"quantity": 2})

        #Creating the garden for user 1 to use in tests
        self.garden1 = garden.objects.create(userID=self.user1, size=3)

        for row in range(self.garden1.size):
            for col in range(self.garden1.size):
                squareID = row * self.garden1.size + col
                gardenSquare.objects.get_or_create(gardenID=self.garden1,
                                                   squareID=squareID,
                                                   defaults={"cardID": None})


        self.garden_square1 = gardenSquare.objects.get(gardenID=self.garden1, squareID=0)
        self.garden_square1.cardID = self.card1
        self.garden_square1.save()


    #Tests if the garden page requires the login
    def testGardenlogin(self):
        '''
        Tests if the garden page requires the login
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        '''
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    #Tests the garden works on entry to it with the user
    def testGardenView(self):
        '''
        Tests the garden works on entry to it with the user
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        '''
        self.client.login(username="testuser1", password="1234")
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Garden/garden.html")

    #Tests that when a user has a card and places it in an available square it works
    def testAddCardToGardenSuccess(self):
        '''
        Tests that when a user has a card and places it in an available square it works
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        '''
        self.client.login(username="testuser1", password="1234")

        #Once logged in places card in designated square
        response = self.client.post(
            reverse('add_card'),
            json.dumps({'row': 2, 'col': 2, 'card_id': self.card1.id}),
            content_type='application/json'
        )   

        #Checks that it worked and card was placed
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertIn("Card placed successfully!", response.json()["message"])

        #Verifies that the card has been placed in the correct square
        new_square = gardenSquare.objects.get(gardenID=self.garden1, squareID=4)
        self.assertEqual(new_square.cardID, self.card1)

    #Tests that if the square is occupied the card cant be placed there
    def testAddCardToGardenFailIfOccupied(self):
        '''
        Tests that if the square is occupied the card cant be placed there
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        '''
        self.client.login(username="testuser1", password="1234")

        #Once logged in tries to place card in wrong place where another card is already there
        response = self.client.post(
            reverse('add_card'),
            json.dumps({'row': 1, 'col': 1, 'card_id': self.card1.id}),
            content_type='application/json'
        )

        #Checks that the correct response has been made to a card being placed in occupied square
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], False)
        self.assertIn("This square is already occupied.", response.json()["message"])

    #Test to check that a card can be removed successfully
    def testRemoveCardSuccess(self):
        '''
        Test to check that a card can be removed successfully
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        '''
        self.client.login(username="testuser1", password="1234")

        #Once logged in user "clicks" on square removing it from the square with a card already in it
        response = self.client.post(
            reverse('remove_card'),
            json.dumps({'row': 1, 'col': 1}),
            content_type='application/json'
        )

        #Checks that the card has been removed successfully
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertIn("Card removed successfully!", response.json()["message"])

        #Checks the square to make sure it is empty
        updated_square = gardenSquare.objects.get(gardenID=self.garden1, squareID=0)
        self.assertIsNone(updated_square.cardID)

        #Checks that the users inventory is showing the correct amount after removing a card
        updated_owns_card = ownsCard.objects.get(user=self.user1, card=self.card1)
        self.assertEqual(updated_owns_card.quantity, 3)


    #Tests to check that if user clicks on empty square it doesnt crash
    def testRemoveCardEmptySquare(self):
        '''
        Tests to check that if user clicks on empty square it doesnt crash
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        '''
        self.client.login(username="testuser1", password="1234")

        #Once logged in user tries to click to remove on an empty square
        response = self.client.post(
            reverse('remove_card'),
            json.dumps({'row': 2, 'col': 2}),
            content_type='application/json'
        )

        #Checks correct process has occured when this happens
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], False)

def test_sustainability_reward_card(self):
    """Test earning garden card through sustainability action
    - Create user
    - Complete eco-friendly action
    - Verify card reward
    """
    # Create test user and login
    user = User.objects.create_user(username="eco_player", password="green123")
    self.client.login(username="eco_player", password="green123")

    # Add sustainability reward card
    response = self.client.post(
        reverse('add_card'),
        json.dumps({'row': 0, 'col': 0, 'card_id': 1}),
        content_type='application/json'
    )

    # Verify card placement
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()["success"], True)
    self.assertIn("Card placed successfully!", response.json()["message"])

