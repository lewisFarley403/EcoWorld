from django.test import TestCase
from EcoWorld.models import pack, card, cardRarity, ownsCard

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





    