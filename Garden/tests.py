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
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from Accounts.models import Profile
from EcoWorld.models import cardRarity, ownsCard, card
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


    def test_show_garden_context(self):
        """
        Tests that the show_garden view returns the correct context
        """
        #Log in the test user
        self.client.login(username="testuser1", password="1234")
        
        #Call the show_garden view via the URL pattern
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Garden/garden.html")
        
        context = response.context
        
        #Verify that the garden size is present and squares is a 2D list of that size
        garden_size = context.get('size')
        self.assertIsNotNone(garden_size)
        
        squares = context.get('squares')
        self.assertIsNotNone(squares)
        #Check that squares is a 2D list of dimensions size x size
        self.assertEqual(len(squares), garden_size)
        for row in squares:
            self.assertEqual(len(row), garden_size)
        
        #Verify MEDIA_URL is correctly passed
        self.assertEqual(context.get('MEDIA_URL'), settings.MEDIA_URL)
        
        #Check userinfo contains username, pfp_url, and coins
        userinfo = context.get("userinfo")
        self.assertIsNotNone(userinfo)
        self.assertIn("username", userinfo)
        self.assertIn("pfp_url", userinfo)
        self.assertIn("coins", userinfo)
        
        #Check that the playerInventory only contains items with quantity > 0
        playerInventory = context.get("playerInventory")
        self.assertIsNotNone(playerInventory)
        for item in playerInventory:
            self.assertTrue(item["quantity"] > 0)

    def test_add_card_insufficient_quantity(self):
        """
        Test that trying to add a card when the user doesn't have enough (quantity <= 0)
        returns the proper error message.
        """
        self.client.login(username="testuser1", password="1234")
        
        # Set the quantity for the card to 0 to simulate insufficient quantity.
        owned_card = ownsCard.objects.get(user=self.user1, card=self.card1)
        owned_card.quantity = 0
        owned_card.save()
        
        response = self.client.post(
            reverse('add_card'),
            json.dumps({'row': 2, 'col': 2, 'card_id': self.card1.id}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "You don't have enough of this card.")




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
        self.assertIn("No card in this square", response.json()["message"])

    
    def testAddCardInvalidCard(self):
        """
        Tests that if an invalid card ID is provided it returns error
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        """
        self.client.login(username="testuser1", password="1234")
        
        #Use a card id that doesn't exist
        response = self.client.post(
            reverse('add_card'),
            json.dumps({'row': 2, 'col': 2, 'card_id': 9999}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Invalid card ID")

    def testAddCardNoOwnership(self):
        """
        Tests that if the user does not own the card the view returns the appropriate error message
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        """
        self.client.login(username="testuser1", password="1234")
        
        #Create a new card that the user does not own
        new_card = card.objects.create(title="New Card", image="cards/new_card.png", rarity=self.common_rarity)
        #check no ownsCard record exists for this card by deleting any if present
        ownsCard.objects.filter(user=self.user1, card=new_card).delete()
        
        response = self.client.post(
            reverse('add_card'),
            json.dumps({'row': 2, 'col': 2, 'card_id': new_card.id}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "You don't own this card")

    def testAddCardInvalidMethod(self):
        """
        Tests that if a non POST request is made to the addCard view it returns the proper message
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        """
        self.client.login(username="testuser1", password="1234")
        
        response = self.client.get(reverse('add_card'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Invalid request.")


    def testRemoveCardInvalidSquare(self):
        """
        Tests that if the row/col do not correspond to an existing gardenSquare the view returns "Invalid garden square"
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        """
        self.client.login(username="testuser1", password="1234")
        # Use row=4, col=1 outside the grid
        response = self.client.post(
            reverse('remove_card'),
            json.dumps({'row': 4, 'col': 1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Invalid garden square")

    def testRemoveCardInvalidMethod(self):
        """
        Tests that a non-POST request to removeCard returns the fallback message
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        """
        self.client.login(username="testuser1", password="1234")
        response = self.client.get(reverse('remove_card'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Invalid request")



    @patch('Garden.views.ownsCard.objects.get_or_create')
    def testRemoveCardownsCardException(self, mock_get_or_create):
        """
        Tests that if ownsCard.get_or_create raises a DoesNotExist exception
        Author: Chris Lynch (cl1037@exeter.ac.uk)
        """
        self.client.login(username="testuser1", password="1234")
        mock_get_or_create.side_effect = ownsCard.DoesNotExist

        response = self.client.post(
            reverse('remove_card'),
            json.dumps({'row': 1, 'col': 1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "You don't own this card")

