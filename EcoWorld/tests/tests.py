import json
import os
from django.test import TestCase, Client
from django.core.management import call_command
from Accounts.models import Profile, FriendRequests, Friends
from EcoWorld.models import pack, card, cardRarity, User,ongoingChallenge
from django.urls import reverse
from django.conf import settings
from datetime import timedelta
from django.db.models import Q

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
        pack.objects.create(title="TestPack", cost=50, packimage="packs/basicpack.png", commonProb=0.5, rareProb=0.3, epicProb=0.15, legendaryProb=0.05,color_class="blue")


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
