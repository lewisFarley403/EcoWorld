import json
import os
from unittest.mock import patch
from django.http import QueryDict
from django.test import TestCase, Client, RequestFactory
from django.core.management import call_command
from Accounts import models
from Accounts.models import Profile, FriendRequests, Friends
from EcoWorld.models import Merge, ownsCard, pack, card, cardRarity, User,ongoingChallenge, Merge
from django.urls import reverse
from django.conf import settings
from datetime import timedelta
from django.db.models import Q
from django.test import TestCase
from django.contrib.auth.models import User
from EcoWorld.models import challenge, ongoingChallenge
from datetime import date 
from django.utils import timezone

from EcoWorld.views import mergecards

"""
Testing class for the packmodels
Methods:
    - setUp() : Sets up the card rarity objects so they can be identified by their ID in a different table in the DB and sets up the pack for testing
    - testPackCreation() : Checks that each attribute in the DB has been set correctly by utils.py for use in the website
    - testPackStrMethod() : Checks that the str method works correctly
Author:
    -Chris Lynch (cl1037@exeter.ac.uk)

"""
#Used to test if the pack models database is set up correctly and items are placed properly
class TestPackModels(TestCase):
    #Sets up test item in database
    def setUp(self):
        self.common = cardRarity.objects.create(title="Common")
        self.rare = cardRarity.objects.create(title="Rare")
        self.epic = cardRarity.objects.create(title="Epic")
        self.legendary = cardRarity.objects.create(title="Legendary")
        self.mythic = cardRarity.objects.create(title="Mythic")
        self.TestPack = pack.objects.create(title="TestPack", cost=50, packimage="packs/basicpack.png", commonProb=0.5, rareProb=0.3, epicProb=0.15, legendaryProb=0.05,color_class="blue")


    #Tests that when the item is created it is properly implemented with the correct values
    def testPackCreation(self):
        testPack = pack.objects.get(title="TestPack")
        self.assertEqual(testPack.cost, 50) 
        self.assertEqual(testPack.packimage, "packs/basicpack.png")
        self.assertEqual(testPack.commonProb, 0.5)
        self.assertEqual(testPack.rareProb,0.3)
        self.assertEqual(testPack.epicProb, 0.15)
        self.assertEqual(testPack.legendaryProb, 0.05)
        self.assertEqual(testPack.color_class, "blue")

    #Test that the __Str__ object works properly when initialising an item in the database
    def testPackStrMethod(self):
        testPack = pack.objects.get(title="TestPack")
        self.assertEqual(str(testPack), "TestPack")




"""
Testing class for the card models in the database and making sure they are all set correctly

Methods: 
    - setUp() : Sets up each card rarity object so it can be linked to another table with its ID, sets up every card types rarity to check they all work
    - testCardCommon() : Tests if the common card rarity works properly
    - testCardRare() : Tests if the rare card rarity works properly
    - testCardEpic() : Tests if the epic card rarity works properly
    - testCardLegendary() : Tests if the legendary card rarity works properly
    - testCardMythic() : Tests if the mythic card rarity works properly
    - testCardStrMethod() : Checks if the str method for cards works properly

Author:
    -Chris Lynch (cl1037@exeter.ac.uk)

"""
#Tests that the card models database works and everything is implemented properly
class TestCardModels(TestCase):
    
    #Sets up each card rarity to make sure foreign key for ID is matched and then sets up each card rarity in the test db
    def setUp(self):
        self.common = cardRarity.objects.create(title="Common")
        self.rare = cardRarity.objects.create(title="Rare")
        self.epic = cardRarity.objects.create(title="Epic")
        self.legendary = cardRarity.objects.create(title="Legendary")
        self.mythic = cardRarity.objects.create(title="Mythic")

        card.objects.create(title="TestCardCommon", description="Etc1234", rarity_id= self.common.id, image="cards/test1.png")
        card.objects.create(title="TestCardRare", description="Etc1234", rarity_id= self.rare.id, image="cards/test2.png")
        card.objects.create(title="TestCardEpic", description="Etc1234", rarity_id= self.epic.id, image="cards/test3.png")
        card.objects.create(title="TestCardLegendary", description="Etc1234", rarity_id= self.legendary.id, image="cards/test4.png")
        card.objects.create(title="TestCardMythic", description="Etc1234", rarity_id= self.mythic.id, image="cards/test5.png")

    #Tests common cards implementation works with correct ID for rarity as well
    def testCardCommon(self):
        testCardCommon = card.objects.get(title="TestCardCommon",description="Etc1234", rarity_id= 1, image="cards/test1.png")
        self.assertEqual(testCardCommon.title, "TestCardCommon")
        self.assertEqual(testCardCommon.description, "Etc1234")
        self.assertEqual(testCardCommon.rarity_id, 1)
        self.assertEqual(testCardCommon.image,"cards/test1.png")

    #Tests rare cards implementation works with correct ID for rarity as well
    def testCardRare(self):
        testCardRare = card.objects.get(title="TestCardRare",description="Etc1234", rarity_id= 2, image="cards/test2.png")
        self.assertEqual(testCardRare.title, "TestCardRare")
        self.assertEqual(testCardRare.description, "Etc1234")
        self.assertEqual(testCardRare.rarity_id, 2)
        self.assertEqual(testCardRare.image,"cards/test2.png")

    #Tests epic cards implementation works with correct ID for rarity as well
    def testCardEpic(self):
        testCardEpic = card.objects.get(title="TestCardEpic",description="Etc1234", rarity_id= 3, image="cards/test3.png")
        self.assertEqual(testCardEpic.title, "TestCardEpic")
        self.assertEqual(testCardEpic.description, "Etc1234")
        self.assertEqual(testCardEpic.rarity_id, 3)
        self.assertEqual(testCardEpic.image,"cards/test3.png")

    #Tests legendary cards implementation works with correct ID for rarity as well
    def testCardLegendary(self):
        testCardLegendary = card.objects.get(title="TestCardLegendary",description="Etc1234", rarity_id= 4, image="cards/test4.png")
        self.assertEqual(testCardLegendary.title, "TestCardLegendary")
        self.assertEqual(testCardLegendary.description, "Etc1234")
        self.assertEqual(testCardLegendary.rarity_id, 4)
        self.assertEqual(testCardLegendary.image,"cards/test4.png")

    #Tests mythic cards implementation works with correct ID for rarity as well
    def testCardMythic(self):
        testCardMythic = card.objects.get(title="TestCardMythic",description="Etc1234", rarity_id= 5, image="cards/test5.png")
        self.assertEqual(testCardMythic.title, "TestCardMythic")
        self.assertEqual(testCardMythic.description, "Etc1234")
        self.assertEqual(testCardMythic.rarity_id, 5)
        self.assertEqual(testCardMythic.image,"cards/test5.png")

    #Tests the str method works properly on the initialisation of a card
    def testCardStrMethod(self):
        testCardCommon = card.objects.get(title="TestCardCommon")
        self.assertEqual(str(testCardCommon), "TestCardCommon")




"""
Test class to make sure that when the user accesses the store all the correct things load and packs are bought properly or dealt with if not
Methods:
    setUp() : Method to set up test user accounts to access the store with coins or with no coins
    testStoreLoadsProperly() : Tests that users who are logged in only can buy a pack from the store and access the store
    testBuyPackSuccess() : Tests that if the user has coins they can buy a pack
    testBuyPackFail() : Tests that if the user hasnt got sufficient funding then they cant buy a pack

Author:
Chris Lynch cl1037@exeter.ac.uk
"""
class TestStore(TestCase):
    #Sets up the test with necessary variables for later
    def setUp(self):
        self.client = Client()

        #Creates users for test
        self.user1 = User.objects.create_user(username="testuser1", password="1234")
        self.user2 = User.objects.create_user(username="testuser2", password="1234")

        #Creates the user profiles 
        self.profile1, _ = Profile.objects.get_or_create(user=self.user1)
        self.profile1.number_of_coins = 0
        self.profile1.profile_picture = "pfp1.png"
        self.profile1.save()

        self.profile2, _ = Profile.objects.get_or_create(user=self.user2)
        self.profile2.number_of_coins = 9999999
        self.profile2.profile_picture = "pfp2.png"
        self.profile2.save()

        #Definitions for each of the 3 packs to be used in the tests
        self.pack1 = pack.objects.create(
            title="Basic Pack",
            cost=20,
            packimage="packs/basicpack.png",
            commonProb=0.5,
            rareProb=0.35,
            epicProb=0.1,
            legendaryProb=0.05,
            color_class="blue",
        )

        self.pack2 = pack.objects.create(
            title="Rare Pack",
            cost=45,
            packimage="packs/rarepack.png",
            commonProb=0.35,
            rareProb=0.35,
            epicProb=0.175,
            legendaryProb=0.125,
            color_class="blue",
        )
        
        self.pack3 = pack.objects.create(
            title="Icon Pack",
            cost=100,
            packimage="packs/iconpack.png",
            commonProb=0.1,
            rareProb=0.4,
            epicProb=0.25,
            legendaryProb=0.25,
            color_class="blue",
        )

    #Tests that when the user is logged in they can view the page correctly and if not they cant and checks if the template receives the info given to it
    def testStoreLoadsProperly(self):
        self.client.login(username="testuser1", password="1234")
        response = self.client.get(reverse('EcoWorld:store'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ecoWorld/store.html")

        #User info tests to make sure the page has what it needs from the user
        self.assertIn("userinfo", response.context)
        self.assertEqual(response.context["userinfo"]["username"], "testuser1")
        self.assertEqual(response.context["userinfo"]["coins"], 0)
        self.assertEqual(response.context["userinfo"]["pfp_url"], "/media/pfps/pfp1.png")

        #Checks that all 3 packs are present
        self.assertIn("packs", response.context)
        self.assertEqual(len(response.context["packs"]), 3)

        #Checks all the packs are correctly shown
        for p in response.context["packs"]:
            if p["title"] == "Basic Pack":
                self.assertEqual(p["image_url"], "/media/packs/basicpack.png")
            elif p["title"] == "Rare Pack":
                self.assertEqual(p["image_url"], "/media/packs/rarepack.png")
            elif p["title"] == "Icon Pack":
                self.assertEqual(p["image_url"], "/media/packs/iconpack.png")

    #Tests if the buy pack works if the user has coins
    def testBuyPackSuccess(self):
        self.client.login(username="testuser2", password="1234")

        #Buys a certain pack from the store and saves the response
        response = self.client.post(
            reverse('EcoWorld:buyPack'),
            json.dumps({'pack_id': self.pack1.id}),
            content_type='application/json'
        )

        self.profile2 = Profile.objects.get(user=self.user2)

        #Checks that given the user logged in and pack bought the correct number of coins has been deducted and pack worked
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})
        self.assertEqual(self.profile2.number_of_coins, 9999979)

    #Test to check if user has insufficient coins they cant buy a pack
    def testBuyPackFail(self):
        self.client.login(username="testuser1", password="1234")

        #Logged in with the user on 0 coins gets response to buying a pack
        response = self.client.post(
            reverse('EcoWorld:buyPack'),
            json.dumps({'pack_id': self.pack1.id}),
            content_type='application/json'
        )

        self.profile1 = Profile.objects.get(user=self.user1)
        #Checks that the coins are still at 0 and that the pack couldnt be bought
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Insufficient coins"})
        self.assertEqual(self.profile1.number_of_coins, 0)


class TestChallenge(TestCase):
    '''
    test the functionality to do with challenges
    author:
        Lewis Farley (lf507@exeter.ac.uk)
    '''
    def setUp(self):

        # Get the absolute path to the initialDb.json file in the root directory
        fixture_path = os.path.join(os.path.dirname(__file__), 'initialDb.json')

        print(fixture_path)
        # Load initialDb.json into the test database
        call_command("loaddata", fixture_path)
        # create user
            
        form_data = {


             'first_name': 'John',
             'last_name': 'Doe',
             'username': 'testuser',
             'email': 'testuser@gmail.com',
             'password1':'P@ssword123',
             'password2':'P@ssword123'
        }
        _ = self.client.post('/accounts/signup/', form_data)

         # g = garden.objects.get(user.username=user)
        user=User.objects.get(username='testuser')
        self.assertEqual(user.profile.number_of_coins,0)
    def test_challenge_view(self):
        '''
        test the challenge view for first time user
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        '''
        self.client.login(username='testuser', password='P@ssword123')
        ongoingChallenges = ongoingChallenge.objects.filter(user=User.objects.get(username='testuser'))
        self.assertEqual(len(ongoingChallenges), 0)
        response = self.client.get(reverse('EcoWorld:challenge'))
        ongoingChallenges = ongoingChallenge.objects.filter(user=User.objects.get(username='testuser'))
        self.assertEqual(len(ongoingChallenges), settings.NUM_CHALLENGES)
    def test_mark_challenge_complete(self):
        '''
        test the mark challenge complete functionality
        Author:
            Lewis Farley (
        '''
        self.client.login(username='testuser', password='P@ssword123')
        response = self.client.get(reverse('EcoWorld:challenge'))
        ongoingChallenges = ongoingChallenge.objects.filter(user=User.objects.get(username='testuser'))
        self.assertEqual(len(ongoingChallenges), settings.NUM_CHALLENGES)
        challenge = ongoingChallenges[0]
        self.assertEqual(challenge.submitted_on, None)
        
        response = self.client.post(
            reverse('EcoWorld:completeChallenge'),  # The URL you're posting to
            json.dumps({'id': challenge.id}),  # The data you want to send, serialized as JSON
            content_type='application/json'  # The content type must be set to application/json
        )
        ongoingChallenges = ongoingChallenge.objects.filter(user=User.objects.get(username='testuser'))
        self.assertNotEqual(ongoingChallenges[0].submitted_on, None)
    def test_challenge_reset(self):
        '''
        test the challenge reset functionality
        Author:
            Lewis Farley (
        '''
        settings.CHALLENGE_EXPIRY = timedelta(seconds=5)  # The time in seconds before a challenge expires
        # delete ongoing challenges
        ongoingChallenges = ongoingChallenge.objects.filter(user=User.objects.get(username='testuser'))
        ongoingChallenges.delete()
        # check that the challenges have been deleted
        ongoingChallenges = ongoingChallenge.objects.filter(user=User.objects.get(username='testuser'))
        self.assertEqual(len(ongoingChallenges), 0)
        self.client.login(username='testuser', password='P@ssword123')
        response = self.client.get(reverse('EcoWorld:challenge'))
        # mark the challenges as completed
        ongoingChallenges = ongoingChallenge.objects.filter(user=User.objects.get(username='testuser'))
        i =ongoingChallenges[0].id
        response = self.client.post(
            reverse('EcoWorld:completeChallenge'),  # The URL you're posting to
            json.dumps({'id': i}),  # The data you want to send, serialized as JSON
            content_type='application/json'  # The content type must be set to application/json
        )
        # wait for them to reset
        import time
        time.sleep(settings.CHALLENGE_EXPIRY.total_seconds())

        # check that the challenges have been reset
        self.client.get(reverse('EcoWorld:challenge'))
        ongoingChallenges = ongoingChallenge.objects.filter(user=User.objects.get(username='testuser'))
        self.assertEqual(ongoingChallenges[0].submitted_on,None)
    def test_coin_reward(self):
        '''
        test the challenge reward functionality
        Author:
            Lewis Farley (
        '''
        self.client.login(username='testuser', password='P@ssword123')
        response = self.client.get(reverse('EcoWorld:challenge'))
        ongoingChallenges = ongoingChallenge.objects.filter(user=User.objects.get(username='testuser'))
        i =ongoingChallenges[0].id
        response = self.client.post(
            reverse('EcoWorld:completeChallenge'),  # The URL you're posting to
            json.dumps({'id': i}),  # The data you want to send, serialized as JSON
            content_type='application/json'  # The content type must be set to application/json
        )
        user=User.objects.get(username='testuser')
        self.assertEqual(user.profile.number_of_coins,settings.CHALLENGE_WORTH)



"""
Test class for the friends page to make sure all things load properly from the GET method and all POST options are dealt
with correctly

Methods:
    setUp() : Sets up 3 users for the friends functions
    testGetRequest(): Test to see that all requests are shown properly
    testSendRequest(): Test to see what happens when you send a friend request
    testRequestToNonExistentPerson(): Tests to see what happens if you request a non existent person
    testSendToSelf():Tests what happens when you try to request yourself as a friend
    testDuplicateRequest(): Tests what happens when you try to send a request to the same person twice 
    textExistingFriend(): Test to see what happens if you try to request an existing friend  
    testAcceptRequest(): Tests accepting a friend request
    testRejectRequest(): Tests rejecting a friend request
    testRemoveFriend(): Tests removing a friend using the button


"""
class TestFriendPage(TestCase):
    def setUp(self):
        #Set up 3 users for the friends page and login to user1
        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")
        self.user3 = User.objects.create_user(username="user3", password="testpass")

        self.client.login(username="user1", password="testpass")

    def testGetRequest(self):
        #Test that all things go the page that should on the page loading
        response = self.client.get(reverse("EcoWorld:friends"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("userinfo", response.context)
        self.assertIn("friendreqs", response.context)
        self.assertIn("friends", response.context)

    def testSendRequest(self):
        #Test sending a friend request
        response = self.client.post(reverse("EcoWorld:friends"), {"friendUsername": "user2"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(FriendRequests.objects.filter(senderID=self.user1, receiverID=self.user2).exists())

    def testRequestToNonExistentPerson(self):
        #Tests sending a request to someone who doesnt exist
        response = self.client.post(reverse("EcoWorld:friends"), {"friendUsername": "nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User Not Found!")
    
    def testSendToSelf(self):
        #Testing that the correct response happens if you send a request to yourself
        response = self.client.post(reverse("EcoWorld:friends"), {"friendUsername": "user1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You cant request yourself")


    def testDuplicateRequest(self):
        #Testing that when sending a friend request while one pending it doesnt add another
        FriendRequests.objects.create(senderID=self.user1, receiverID=self.user2)
        response = self.client.post(reverse("EcoWorld:friends"), {"friendUsername": "user2"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Friend request already pending")

    def testExistingFriend(self):
        #Testing that you cant send a request to an existing friend
        Friends.objects.create(userID1=self.user1, userID2=self.user2)
        response = self.client.post(reverse("EcoWorld:friends"), {"friendUsername": "user2"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are already friends with this user!")

    def testAcceptRequest(self):
        #Testing that accepting a friend request works
        FriendRequests.objects.create(senderID=self.user2, receiverID=self.user1)
        response = self.client.post(reverse("EcoWorld:friends"), {"friendar": "user2", "friendaction": "accept"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Friends.objects.filter(userID1=self.user1, userID2=self.user2).exists())
        self.assertFalse(FriendRequests.objects.filter(senderID=self.user2, receiverID=self.user1).exists())

    def testRejectRequest(self):
        #Test that rejecting a friend request works
        FriendRequests.objects.create(senderID=self.user2, receiverID=self.user1)
        response = self.client.post(reverse("EcoWorld:friends"), {"friendar": "user2", "friendaction": "reject"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(FriendRequests.objects.filter(senderID=self.user2, receiverID=self.user1).exists())

    def testRemoveFriend(self):
        #Test to remove a friend
        Friends.objects.create(userID1=self.user1, userID2=self.user2)
        response = self.client.post(reverse("EcoWorld:friends"), {"remove": "user2"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Friends.objects.filter(Q(userID1=self.user1, userID2=self.user2) | Q(userID1=self.user2, userID2=self.user1)).exists())


"""
Test class for the merge page to merge cards together for an upgrade. Tests that it loads properly and the functions in the page work
correctly

Methods:
    setUp(): Sets up cards for the merging functions and a user to be logged in
    testGetRequest(): Tests that on loadup the page functons correctly with the correct items in
    testRarityPost(): When selecting rarity checks correct features are added to page
    testAddCard(): Tests that when adding card to table it works correctly
    testRemoveCard(): Tests when removing card from table it works correctly

    Author:
    Chris Lynch (cl1037@exeter.ac.uk)
"""
class TestMergeCards(TestCase):
    def setUp(self):
        #Creates user and logs in
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        

        self.factory = RequestFactory()
        #Creates rarities for tests
        self.rarity_common = cardRarity.objects.create(id=1, title="Common")
        self.rarity_uncommon = cardRarity.objects.create(id=2, title="Uncommon")
        
        #Creates two cards of same rarity
        self.card1 = card.objects.create(title="Card 1", rarity_id=self.rarity_common.id, image="cards/card1.jpg")
        self.card2 = card.objects.create(title="Card 2", rarity_id=self.rarity_common.id, image="cards/card2.jpg")
        
        #Gives user card for placements
        self.ownCard1 = ownsCard.objects.create(user=self.user, card=self.card1, quantity=5)

    #Test that correct things are returned when page is loaded
    def testGetRequest(self):
        """ Tests the correct things are returned for get request """
        response = self.client.get(reverse("EcoWorld:mergecards"))
        self.assertEqual(response.status_code, 200)
        #Check that the context contains the expected keys
        self.assertIn("userinfo", response.context)
        self.assertIn("merge", response.context)
        
        #Verify that merge (which holds the card images list) is a list with 5 items
        merge_context = response.context["merge"]
        self.assertEqual(len(merge_context), 5)
        
        #check that each item is a dict with 'id' and 'image' keys
        for item in merge_context:
            self.assertIn("id", item)
            self.assertIn("image", item)


    #Tests when selecting a rarity the table works correctly
    def testRarityPost(self):
        """Tests the post request for rarity works"""
        response = self.client.post(reverse("EcoWorld:mergecards"), {"rarity": self.rarity_common.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn("playerItems", response.context)
        self.assertIn("rarity", response.context)
        self.assertIn("merge", response.context)

    #Tests when adding a card to the merge slot it works correctly
    def testAddCard(self):
        """Tests the add card method works"""
        #Add card to merge slot 1
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "addCard": self.card1.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        #Checks that the card actually went into a slot
        merge_instance = Merge.objects.get(userID=self.user)
        merge_slots = [
            merge_instance.cardID1,
            merge_instance.cardID2,
            merge_instance.cardID3,
            merge_instance.cardID4,
            merge_instance.cardID5,
        ]
        self.assertTrue(self.card1 in merge_slots)
        #Makes sure inventory decreased when adding to slot
        own = ownsCard.objects.get(user=self.user, card=self.card1)
        self.assertEqual(own.quantity, 4)

    #Test to check when removing a card from a slot it works correctly
    def testRemoveCard(self):
        """Tests the remove card method works"""
        #Adds a card to merge slot
        merge_instance, created = Merge.objects.get_or_create(userID=self.user)
        merge_instance.cardID1 = self.card1
        merge_instance.save()
        #Checks it got removed from inventory properly
        own = ownsCard.objects.get(user=self.user, card=self.card1)
        own.quantity -= 1
        own.save()

        #Send POST request to remove that card from the slot
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "removeCard": self.card1.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        #Checks that the card was removed from the slot
        merge_instance.refresh_from_db()
        self.assertIsNone(merge_instance.cardID1)
        #Checks that the card was added back to the inventory
        own.refresh_from_db()
        self.assertEqual(own.quantity, 5)



    def testAddCardError(self):
        """Tests that trying to add a card when all merge slots are full returns an error."""
        #Populate the merge instance with a card in all 5 slots.
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        merge_instance.cardID1 = self.card1
        merge_instance.cardID2 = self.card1
        merge_instance.cardID3 = self.card1
        merge_instance.cardID4 = self.card1
        merge_instance.cardID5 = self.card1
        merge_instance.save()

        #Ensure the user owns enough copies of the card
        own = ownsCard.objects.get(user=self.user, card=self.card1)
        own.quantity = 5
        own.save()

        #Attempt to add the same card again
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "addCard": self.card1.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        #Check that the error message is in the response context
        self.assertIn("error", response.context)
        self.assertEqual(
            response.context["error"],
            "There are already 5 cards in the merge slots remove one first!"
        )

    def testAddCardDifferentRarityError(self):
        """Tests that adding a card of a different rarity than the first card returns an error"""
        #Create an uncommon card and give the user ownership of it
        card_uncommon = card.objects.create(title="Card Uncommon", rarity_id=self.rarity_uncommon.id, image="cards/card_uncommon.jpg")
        ownsCard.objects.create(user=self.user, card=card_uncommon, quantity=5)

        #Populate the merge instance with a common card in slot 1
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        merge_instance.cardID1 = self.card1  #self.card1 is a common rarity
        merge_instance.save()

        #Attempt to add the uncommon card while merge already has a common card
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "addCard": card_uncommon.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        #Verify that the error message is returned
        self.assertIn("error", response.context)
        self.assertEqual(
            response.context["error"],
            "The card you tried to add was not of the same rarity as the first card in the merge."
        )

    def testAddCardFillsSlot2(self):
        """Tests that if slot1 is already filled, the new card is added to slot2"""
        #Populate merge slot 1 with card
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        merge_instance.cardID1 = self.card1
        merge_instance.save()

        #Create an ownership for card 2
        ownsCard.objects.create(user=self.user, card=self.card2, quantity=5)

        #Post request to add card2
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "addCard": self.card2.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        merge_instance.refresh_from_db()
        #Since slot1 is taken, card2 should be added to slot2
        self.assertEqual(merge_instance.cardID2, self.card2)

        #Check that the inventory for card2 decreased
        own_card2 = ownsCard.objects.get(user=self.user, card=self.card2)
        self.assertEqual(own_card2.quantity, 4)

    def testAddCardFillsSlot3(self):
        """Tests that if slots 1 and 2 are filled, the new card is added to slot3"""
        # Pre-populate merge with card1 in slot1 and card2 in slot2.
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        merge_instance.cardID1 = self.card1
        merge_instance.cardID2 = self.card2
        merge_instance.save()

        #Create a new card (card3) of the same rarity and give the user ownership
        card3 = card.objects.create(title="Card 3", rarity_id=self.rarity_common.id, image="cards/card3.jpg")
        ownsCard.objects.create(user=self.user, card=card3, quantity=5)

        #Post request to add card3
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "addCard": card3.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        merge_instance.refresh_from_db()
        #Since slots 1 and 2 are taken, card3 should be added to slot3
        self.assertEqual(merge_instance.cardID3, card3)

        #Check that the inventory for card3 decreased
        own_card3 = ownsCard.objects.get(user=self.user, card=card3)
        self.assertEqual(own_card3.quantity, 4)



    def testAddCardFillsSlot4(self):
        """Tests that if slots 1, 2, and 3 are filled, the new card is added to slot4"""
        # Pre-populate merge with card1 in slot1, card2 in slot2, and a new card in slot3.
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        merge_instance.cardID1 = self.card1
        merge_instance.cardID2 = self.card2
        #Create card3 and give the user ownership
        card3 = card.objects.create(title="Card 3", rarity_id=self.rarity_common.id, image="cards/card3.jpg")
        ownsCard.objects.create(user=self.user, card=card3, quantity=5)
        merge_instance.cardID3 = card3
        merge_instance.save()

        #Create card4 and give the user ownership
        card4 = card.objects.create(title="Card 4", rarity_id=self.rarity_common.id, image="cards/card4.jpg")
        ownsCard.objects.create(user=self.user, card=card4, quantity=5)

        #Post request to add card4
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "addCard": card4.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        merge_instance.refresh_from_db()
        #Since slots 1-3 are taken, card4 should be added to slot4
        self.assertEqual(merge_instance.cardID4, card4)

        #Check that the inventory for card4 decreased
        own_card4 = ownsCard.objects.get(user=self.user, card=card4)
        self.assertEqual(own_card4.quantity, 4)

    def testAddCardFillsSlot5(self):
        """Tests that if slots 1 through 4 are filled, the new card is added to slot5"""
        #Pre-populate merge with card1 in slot1, card2 in slot2, card3 in slot3, and card4 in slot4
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        merge_instance.cardID1 = self.card1
        merge_instance.cardID2 = self.card2

        card3 = card.objects.create(title="Card 3", rarity_id=self.rarity_common.id, image="cards/card3.jpg")
        ownsCard.objects.create(user=self.user, card=card3, quantity=5)
        merge_instance.cardID3 = card3

        card4 = card.objects.create(title="Card 4", rarity_id=self.rarity_common.id, image="cards/card4.jpg")
        ownsCard.objects.create(user=self.user, card=card4, quantity=5)
        merge_instance.cardID4 = card4

        merge_instance.save()

        #Create card5 and give the user ownership
        card5 = card.objects.create(title="Card 5", rarity_id=self.rarity_common.id, image="cards/card5.jpg")
        ownsCard.objects.create(user=self.user, card=card5, quantity=5)

        #Post request to add card5
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "addCard": card5.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        merge_instance.refresh_from_db()
        #Since slots 1-4 are taken, card5 should be added to slot5
        self.assertEqual(merge_instance.cardID5, card5)

        #Check that the inventory for card5 decreased
        own_card5 = ownsCard.objects.get(user=self.user, card=card5)
        self.assertEqual(own_card5.quantity, 4)

    def testAddCardInsufficientQuantity(self):
        """Tests that adding a card with insufficient quantity returns the proper error"""
        #Set the quantity of the owned card to 0
        own = ownsCard.objects.get(user=self.user, card=self.card1)
        own.quantity = 0
        own.save()
        
        #Attempt to add the card
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "addCard": self.card1.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        #Verify that the error message is returned
        self.assertIn("error", response.context)
        self.assertEqual(
            response.context["error"],
            "You need to get more of this card to add it to the merge or take one out of the merge box"
        )

    def testRemoveCardSlot2(self):
        """Tests that a card is correctly removed from merge slot 2"""
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        #Ensure slot1 is empty and slot2 is filled
        merge_instance.cardID1 = None
        merge_instance.cardID2 = self.card1
        merge_instance.save()
        
        #Simulate that card1 was previously added (inventory decreased)
        own = ownsCard.objects.get(user=self.user, card=self.card1)
        own.quantity -= 1
        own.save()
        
        #Send POST request to remove the card
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "removeCard": self.card1.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        
        merge_instance.refresh_from_db()
        #Verify that slot2 is now cleared
        self.assertIsNone(merge_instance.cardID2)
        
        own.refresh_from_db()
        #Verify that inventory quantity has been increased back by 1
        self.assertEqual(own.quantity, 5)
    
    def testRemoveCardSlot3(self):
        """Tests that a card is correctly removed from merge slot 3"""
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        #Ensure slots 1 and 2 are empty, and slot3 is filled
        merge_instance.cardID1 = None
        merge_instance.cardID2 = None
        merge_instance.cardID3 = self.card1
        merge_instance.save()
        
        #Simulate a prior deduction in inventory
        own = ownsCard.objects.get(user=self.user, card=self.card1)
        own.quantity -= 1
        own.save()
        
        #Remove the card from the merge slot
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "removeCard": self.card1.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        
        merge_instance.refresh_from_db()
        #Verify that slot3 is now empty
        self.assertIsNone(merge_instance.cardID3)
        
        own.refresh_from_db()
        self.assertEqual(own.quantity, 5)
    
    def testRemoveCardSlot4(self):
        """Tests that a card is correctly removed from merge slot 4"""
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        #Ensure slots 1-3 are empty, and slot4 is filled
        merge_instance.cardID1 = None
        merge_instance.cardID2 = None
        merge_instance.cardID3 = None
        merge_instance.cardID4 = self.card1
        merge_instance.save()
        
        #Deduct one from inventory to simulate prior addition
        own = ownsCard.objects.get(user=self.user, card=self.card1)
        own.quantity -= 1
        own.save()
        
        #Remove the card via POST
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "removeCard": self.card1.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        
        merge_instance.refresh_from_db()
        self.assertIsNone(merge_instance.cardID4)
        
        own.refresh_from_db()
        self.assertEqual(own.quantity, 5)
    
    def testRemoveCardSlot5(self):
        """Tests that a card is correctly removed from merge slot 5"""
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        #Ensure slots 1-4 are empty, and slot5 is filled
        merge_instance.cardID1 = None
        merge_instance.cardID2 = None
        merge_instance.cardID3 = None
        merge_instance.cardID4 = None
        merge_instance.cardID5 = self.card1
        merge_instance.save()
        
        #Deduct inventory for card1
        own = ownsCard.objects.get(user=self.user, card=self.card1)
        own.quantity -= 1
        own.save()
        
        #POST request to remove card from slot5
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "removeCard": self.card1.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        
        merge_instance.refresh_from_db()
        self.assertIsNone(merge_instance.cardID5)
        
        own.refresh_from_db()
        self.assertEqual(own.quantity, 5)

    def testMergeCardImagesContext(self):
        """Tests that the merge context is built correctly when some slots contain a card"""
        #Pre-populate the merge instance: add self.card1 to slot 3
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        merge_instance.cardID3 = self.card1
        merge_instance.save()

        #Perform a GET request to the mergecards view
        response = self.client.get(reverse("EcoWorld:mergecards"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("merge", response.context)
        merge_context = response.context["merge"]
        
        #Verify that the merge list has 5 items
        self.assertEqual(len(merge_context), 5)
        
        # Build the expected context list:
        expected = [
            {'id': None, 'image': None},
            {'id': None, 'image': None},
            {'id': 'cardID3', 'image': self.card1.image.url},
            {'id': None, 'image': None},
            {'id': None, 'image': None},
        ]
        self.assertEqual(merge_context, expected)

    def testRemoveCardNotInMergeSlot(self):
        """Tests that trying to remove a card that is not in any merge slot returns the appropriate error"""
        #Ensure the merge instance exists and that all merge slots are empty
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        merge_instance.cardID1 = None
        merge_instance.cardID2 = None
        merge_instance.cardID3 = None
        merge_instance.cardID4 = None
        merge_instance.cardID5 = None
        merge_instance.save()
        
        #Post a request to remove self.card1, which is not in any merge slot
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "removeCard": self.card1.id,
            "rarityforbutton": self.rarity_common.id,
        })
        self.assertEqual(response.status_code, 200)
        #Verify that the error message is returned
        self.assertIn("error", response.context)
        self.assertEqual(response.context["error"], "This card is not in a merge slot")
        
        #Also verify that the context contains the expected keys
        self.assertIn("playerItems", response.context)
        self.assertIn("rarity", response.context)
        self.assertIn("merge", response.context)
        
        #Check that the merge context (cardImages) is built correctly (5 slots, each empty)
        merge_context = response.context["merge"]
        self.assertEqual(len(merge_context), 5)
        for item in merge_context:
            self.assertEqual(item, {'id': None, 'image': None})


    def testMergeCardsFuncError(self):
        """Tests that submitting mergebutton equal to '5' returns the appropriate error."""
        # Create an owned card for common rarity (id=1)
        # (Already created in setUp: self.card1 with rarity common)
        # Ensure there is at least one card in the inventory for the rarity filter.
        # In this branch, the view filters on card__rarity_id=rarity (where rarity is passed via POST)
        # and then adjusts the image path.
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "mergebutton": "5",  # This should trigger the error condition.
            "rarity": self.rarity_common.id,  # This is used to fetch the inventory.
        })
        self.assertEqual(response.status_code, 200)
        # Check that the error message is as expected.
        self.assertIn("error", response.context)
        self.assertEqual(
            response.context["error"],
            "This card rarity cannot be merged!"
        )
        # Verify that the context contains playerItems and merge keys.
        self.assertIn("playerItems", response.context)
        self.assertIn("merge", response.context)
        # The merge list should have 5 items (even if empty).
        self.assertEqual(len(response.context["merge"]), 5)


    def testMergeCardsProcessing(self):
        """Tests that when mergebutton is submitted and merge slots are full, the merge is processed."""
        # Create a card for uncommon rarity (rarity id=2) which will be the result of merging.
        card_uncommon = card.objects.create(
            title="Card Uncommon", 
            rarity_id=self.rarity_uncommon.id, 
            image="cards/card_uncommon.jpg"
        )
        # Ensure user owns the uncommon card (even if quantity is 0 initially).
        ownsCard.objects.create(user=self.user, card=card_uncommon, quantity=0)

        # Populate the merge instance with a card in all 5 slots (using self.card1 which is of common rarity)
        merge_instance, _ = Merge.objects.get_or_create(userID=self.user)
        merge_instance.cardID1 = self.card1
        merge_instance.cardID2 = self.card1
        merge_instance.cardID3 = self.card1
        merge_instance.cardID4 = self.card1
        merge_instance.cardID5 = self.card1
        merge_instance.save()

        # Simulate a merge action.
        # Here, we pass mergebutton with a value that is not "5". In the view, the code converts the value 
        # to an int and increments it. For example, if we send "1", then mergeCardsFunc becomes 1 and after increment, 2.
        response = self.client.post(reverse("EcoWorld:mergecards"), {
            "mergebutton": "1",  # a valid merge action
            "rarity": self.rarity_common.id,  # initial rarity used to fetch inventory
        })

        # The merge should have been processed, meaning:
        # - The merge slots are cleared.
        merge_instance.refresh_from_db()
        self.assertIsNone(merge_instance.cardID1)
        self.assertIsNone(merge_instance.cardID2)
        self.assertIsNone(merge_instance.cardID3)
        self.assertIsNone(merge_instance.cardID4)
        self.assertIsNone(merge_instance.cardID5)
        # - The user should receive a card of the next rarity (i.e. rarity 2, uncommon in our test setup).
        # Since the template returned is "EcoWorld/merge_opening_page.html", we can check for that.
        self.assertTemplateUsed(response, "EcoWorld/merge_opening_page.html")
        # - Also, the user's ownership for the uncommon card should be incremented.
        user_own_uncommon = ownsCard.objects.get(user=self.user, card=card_uncommon)
        self.assertEqual(user_own_uncommon.quantity, 1)







class TestMergeOpeningPage(TestCase):
    def setUp(self):
        self.client = Client()

    def test_merge_opening_page(self):
        """Tests merge page opens"""
        response = self.client.get(reverse("EcoWorld:mergereveal"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "EcoWorld/merge_opening_page.html")





"""
Test card rarity model
Methods:
    setUp() ; Sets up a card rarity
    testCardStrMethod() : Tests the string method
Author:
Chris Lynch (cl1037@exeter.ac.uk)
"""
class TestcardRarity(TestCase):
    def setUp(self):
        self.common = cardRarity.objects.create(title="Common")

    #Tests string method
    def testCardStrMethod(self):
        """
        Tests the string method works
        """
        self.assertEqual(str(self.common), "Common")

"""
Test class for owns card model
Methods:
setUp(): Makes a user and gives them a card
checkStrMethod(): Checks the str method works

Author:
Chris Lynch (cl1037@exeter.ac.uk)
"""
class TestOwnsCard(TestCase):
    def setUp(self):
        #Sets up user 
        self.user = User.objects.create_user(username="testuser", password="testpass")
        common_rarity = cardRarity.objects.create(title="Common")
        #Card ownership
        self.test_card = card.objects.create(title="log", rarity=common_rarity)
        
        
        #Create an ownsCard instance
        self.owns_card = ownsCard.objects.create(user=self.user, card=self.test_card, quantity=5)


    def testStrMethod(self):
        """
        Test Str method works
        """
        expected_string = f"{self.user.username} owns {self.test_card.title}"
        self.assertEqual(str(self.owns_card), expected_string)


class TestMergeModel(TestCase):
    def setUp(self):
        #Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")
        
        #Create a test cardRarity instance for cards
        self.common = cardRarity.objects.create(title="common")
        
        #Create test card instances.
        self.card1 = card.objects.create(title="Card1", rarity=self.common)
        self.card2 = card.objects.create(title="Card2", rarity=self.common)
        self.card3 = card.objects.create(title="Card3", rarity=self.common)
        self.card4 = card.objects.create(title="Card4", rarity=self.common)
        self.card5 = card.objects.create(title="Card5", rarity=self.common)
        
        #Create a Merge instance linking the user and the cards
        self.merge = Merge.objects.create(
            userID=self.user,
            cardID1=self.card1,
            cardID2=self.card2,
            cardID3=self.card3,
            cardID4=self.card4,
            cardID5=self.card5
        )

    def testMergeStr(self):
        # Test that the __str__ method returns the expected string
        expected_str = f"Merge operation for {self.user.username}"
        self.assertEqual(str(self.merge), expected_str)
        
        
class ChallengesTest(TestCase):
    """
    Comprehensive test suite for the Challenges page including:
    - Initial challenge assignment
    - Drink cooldown logic
    - Daily objective incrementing
    - Challenge completion and reward
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        profile = self.user.profile
        profile.number_of_coins = 0
        profile.profile_picture = "test.png"
        profile.save()
        self.client.login(username="testuser", password="testpass")

        self.challenge = challenge.objects.create(
            name="Test Challenge",
            description="Test Description",
            worth=10,
            goal=3
        )
        self.ongoing = ongoingChallenge.objects.create(
            user=self.user,
            challenge=self.challenge
        )

    def test_challenge_page_context(self):
        """
        Verify that the challenge page renders with the correct context for a logged-in user.
        """
        response = self.client.get(reverse("EcoWorld:challenge"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("daily_objectives", response.context)
        self.assertIn("coins", response.context)
        self.assertEqual(response.context["coins"], 0)
        self.assertIn("is_drink_available", response.context)

    def test_drink_cooldown_logic(self):
        """
        Confirm that the drink button availability logic is correct based on cooldown setting.
        """
        from qrCodes.models import drinkEvent, waterFountain

        fountain = waterFountain.objects.create(name="F1", location="Test")
        drinkEvent.objects.create(user=self.user, drank_on=timezone.now(), fountain=fountain)
        response = self.client.get(reverse("EcoWorld:challenge"))
        self.assertFalse(response.context["is_drink_available"])

        # simulate cooldown passed
        drinkEvent.objects.update(drank_on=timezone.now() - settings.DRINKING_COOLDOWN - timedelta(seconds=10))
        response = self.client.get(reverse("EcoWorld:challenge"))
        self.assertTrue(response.context["is_drink_available"])

    def test_increment_daily_objective(self):
        """
        Test that a daily objective can be incremented up to its goal.
        """
        url = reverse("EcoWorld:increment_objective")
        for _ in range(self.challenge.goal):
            response = self.client.post(url, json.dumps({"objective_id": self.ongoing.id}), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.ongoing.refresh_from_db()

        self.assertEqual(self.ongoing.progress, self.challenge.goal)

    def test_complete_challenge(self):
        """
        Test that completing a challenge sets submitted_on and adds coin reward.
        """
        url = reverse("EcoWorld:completeChallenge")
        response = self.client.post(url, json.dumps({"id": self.ongoing.id}), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        self.ongoing.refresh_from_db()
        self.user.refresh_from_db()

        self.assertIsNotNone(self.ongoing.submitted_on)
        self.assertEqual(self.user.profile.number_of_coins, self.challenge.worth)

    def test_prevent_increment_beyond_goal(self):
        """
        Test that progress does not exceed the challenge goal even if the endpoint is hit multiple times.
        """
        url = reverse("EcoWorld:increment_objective")
        for _ in range(self.challenge.goal + 3):  # over-increment
            response = self.client.post(url, json.dumps({"objective_id": self.ongoing.id}), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.ongoing.refresh_from_db()

        self.assertLessEqual(self.ongoing.progress, self.challenge.goal)

    def test_multiple_objectives_progress_sum(self):
        """
        Ensure multiple objectives aggregate correctly and progress is tracked individually.
        """
        # Add a second challenge & objective
        ch2 = challenge.objects.create(name="Second", description="2", worth=5, goal=2)
        obj2 = ongoingChallenge.objects.create(user=self.user, challenge=ch2)

        url = reverse("EcoWorld:increment_objective")

        self.client.post(url, json.dumps({"objective_id": self.ongoing.id}), content_type='application/json')
        self.client.post(url, json.dumps({"objective_id": obj2.id}), content_type='application/json')
        self.ongoing.refresh_from_db()
        obj2.refresh_from_db()

        self.assertEqual(self.ongoing.progress, 1)
        self.assertEqual(obj2.progress, 1)

    def test_challenge_submission_sets_timestamp(self):
        """
        Confirm submitted_on is a valid datetime after completing a challenge.
        """
        url = reverse("EcoWorld:completeChallenge")
        self.client.post(url, json.dumps({"id": self.ongoing.id}), content_type='application/json')

        self.ongoing.refresh_from_db()
        self.assertIsNotNone(self.ongoing.submitted_on)
        self.assertTrue(timezone.is_aware(self.ongoing.submitted_on))
