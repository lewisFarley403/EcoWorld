from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from EcoWorld.models import ongoingChallenge, dailyObjective, challenge
from Accounts.models import Friends, Profile
from django.utils import timezone
import json

class ForumViewsTest(TestCase):
    def setUp(self):
        # Create test users
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.friend = User.objects.create_user(username='frienduser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        
        # Create profiles for users (using get_or_create to handle signal-created profiles)
        Profile.objects.get_or_create(user=self.user)
        Profile.objects.get_or_create(user=self.friend)
        Profile.objects.get_or_create(user=self.other_user)
        
        # Create a friendship
        Friends.objects.create(userID1=self.user, userID2=self.friend)
        
        # Create a test challenge
        self.challenge = challenge.objects.create(
            name="Test Challenge",
            description="Test Description",
            created_by=self.user,
            created_on=timezone.now().date(),
            worth=100
        )
        
        # Create test ongoing challenges
        self.user_challenge = ongoingChallenge.objects.create(
            user=self.user,
            challenge=self.challenge,
            submitted_on=timezone.now(),
            submission="Test submission",
            completion_count=1
        )
        
        self.friend_challenge = ongoingChallenge.objects.create(
            user=self.friend,
            challenge=self.challenge,
            submitted_on=timezone.now(),
            submission="Friend submission",
            completion_count=1
        )
        
        # Create test daily objectives
        self.user_objective = dailyObjective.objects.create(
            user=self.user,
            name="Test Objective",
            progress=50,
            goal=100,
            date_created=timezone.now(),
            submission="Test objective submission",
            completed=True,
            coins=10
        )
        
        self.friend_objective = dailyObjective.objects.create(
            user=self.friend,
            name="Friend Objective",
            progress=75,
            goal=100,
            date_created=timezone.now(),
            submission="Friend objective submission",
            completed=True,
            coins=15
        )

    def test_feed_view_authenticated(self):
        """Test the feed view when user is authenticated
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('forum:feed'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed/feed.html')
        self.assertIn('userinfo', response.context)
        self.assertEqual(response.context['userinfo']['username'], 'testuser')

    def test_feed_view_unauthenticated(self):
        """Test the feed view when user is not authenticated
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        response = self.client.get(reverse('forum:feed'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_get_challenge_info_my_filter(self):
        """Test get_challenge_info view with 'my' filter
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'my'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Verify structure and content
        self.assertIn('ongoing_challenges', data)
        self.assertIn('daily_objectives', data)
        self.assertEqual(len(data['ongoing_challenges']), 1)
        self.assertEqual(data['ongoing_challenges'][0]['name'], 'Test Challenge')
        self.assertEqual(len(data['daily_objectives']), 1)
        self.assertEqual(data['daily_objectives'][0]['name'], 'Test Objective')

    def test_get_challenge_info_friends_filter(self):
        """Test get_challenge_info view with 'friends' filter
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'friends'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Verify only friend's data is returned
        self.assertIn('ongoing_challenges', data)
        self.assertIn('daily_objectives', data)
        self.assertEqual(len(data['ongoing_challenges']), 1)
        self.assertEqual(data['ongoing_challenges'][0]['username'], 'frienduser')
        self.assertEqual(len(data['daily_objectives']), 1)
        self.assertEqual(data['daily_objectives'][0]['username'], 'frienduser')

    def test_get_challenge_info_university_filter(self):
        """Test get_challenge_info view with 'university' filter
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'university'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Verify all challenges are returned
        self.assertIn('ongoing_challenges', data)
        self.assertIn('daily_objectives', data)
        self.assertEqual(len(data['ongoing_challenges']), 2)  # Should include both user and friend challenges
        self.assertEqual(len(data['daily_objectives']), 2)  # Should include both user and friend objectives

    def test_get_challenge_info_no_friends(self):
        """Test get_challenge_info view with 'friends' filter when user has no friends
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Create a new user with no friends
        lonely_user = User.objects.create_user(username='lonely', password='testpass123')
        Profile.objects.get_or_create(user=lonely_user)
        
        self.client.login(username='lonely', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'friends'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Verify the response indicates no friends
        self.assertTrue(data['has_no_friends'])
        self.assertEqual(len(data['ongoing_challenges']), 0)
        self.assertEqual(len(data['daily_objectives']), 0)

    def test_get_challenge_info_unauthenticated(self):
        """Test get_challenge_info view when user is not authenticated
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        response = self.client.get(reverse('forum:get_challenge_info'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_friend_feed_visibility_user1_adds_user2(self):
        """T1: Test feed visibility when user1 adds user2 as friend
        - Add 3 users
        - Have user1 add user2 as friend
        - Have user1 make a post
        - Verify user2 can see it but user3 cannot in friends-only feed
        - Verify all users can see it in university feed
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Create 3 test users
        user1 = User.objects.create_user(username='user1', password='testpass123')
        user2 = User.objects.create_user(username='user2', password='testpass123')
        user3 = User.objects.create_user(username='user3', password='testpass123')
        
        # Create profiles for users
        Profile.objects.get_or_create(user=user1)
        Profile.objects.get_or_create(user=user2)
        Profile.objects.get_or_create(user=user3)
        
        # User1 adds User2 as friend
        Friends.objects.create(userID1=user1, userID2=user2)
        
        # Create a test challenge
        test_challenge = challenge.objects.create(
            name="User1's Challenge",
            description="Test Description",
            created_by=user1,
            created_on=timezone.now().date(),
            worth=100
        )
        
        # User1 makes a post (completes a challenge)
        user1_challenge = ongoingChallenge.objects.create(
            user=user1,
            challenge=test_challenge,
            submitted_on=timezone.now(),
            submission="User1's submission",
            completion_count=1
        )
        
        # Check User2's friends feed (should see User1's post)
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'friends'})
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['ongoing_challenges']), 1)
        self.assertEqual(data['ongoing_challenges'][0]['username'], 'user1')
        
        # Check User3's friends feed (should not see User1's post)
        self.client.login(username='user3', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'friends'})
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['has_no_friends'])
        self.assertEqual(len(data['ongoing_challenges']), 0)

        # Check university feed visibility for all users
        # User1 should see all posts in university feed
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'university'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        # Find User1's post in the university feed
        user1_posts = [c for c in data['ongoing_challenges'] if c['username'] == 'user1']
        self.assertEqual(len(user1_posts), 1)
        self.assertEqual(user1_posts[0]['name'], "User1's Challenge")

        # User2 should see all posts in university feed
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'university'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        # Find User1's post in the university feed
        user1_posts = [c for c in data['ongoing_challenges'] if c['username'] == 'user1']
        self.assertEqual(len(user1_posts), 1)
        self.assertEqual(user1_posts[0]['name'], "User1's Challenge")

        # User3 should see all posts in university feed despite not being friends
        self.client.login(username='user3', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'university'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        # Find User1's post in the university feed
        user1_posts = [c for c in data['ongoing_challenges'] if c['username'] == 'user1']
        self.assertEqual(len(user1_posts), 1)
        self.assertEqual(user1_posts[0]['name'], "User1's Challenge")

    def test_friend_feed_visibility_user2_adds_user1(self):
        """T2: Test feed visibility when user2 adds user1 as friend
        - Add 3 users
        - Have user2 add user1 as friend
        - Have user1 make a post
        - Verify user2 can see it but user3 cannot in friends-only feed
        - Verify all users can see it in university feed
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Create 3 test users
        user1 = User.objects.create_user(username='user1', password='testpass123')
        user2 = User.objects.create_user(username='user2', password='testpass123')
        user3 = User.objects.create_user(username='user3', password='testpass123')
        
        # Create profiles for users
        Profile.objects.get_or_create(user=user1)
        Profile.objects.get_or_create(user=user2)
        Profile.objects.get_or_create(user=user3)
        
        # User2 adds User1 as friend (opposite direction from previous test)
        Friends.objects.create(userID1=user2, userID2=user1)
        
        # Create a test challenge
        test_challenge = challenge.objects.create(
            name="User1's Challenge",
            description="Test Description",
            created_by=user1,
            created_on=timezone.now().date(),
            worth=100
        )
        
        # User1 makes a post (completes a challenge)
        user1_challenge = ongoingChallenge.objects.create(
            user=user1,
            challenge=test_challenge,
            submitted_on=timezone.now(),
            submission="User1's submission",
            completion_count=1
        )
        
        # Check User2's friends feed (should see User1's post)
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'friends'})
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['ongoing_challenges']), 1)
        self.assertEqual(data['ongoing_challenges'][0]['username'], 'user1')
        
        # Check User3's friends feed (should not see User1's post)
        self.client.login(username='user3', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'friends'})
        data = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['has_no_friends'])
        self.assertEqual(len(data['ongoing_challenges']), 0)

        # Check university feed visibility for all users
        # User1 should see all posts in university feed
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'university'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        # Find User1's post in the university feed
        user1_posts = [c for c in data['ongoing_challenges'] if c['username'] == 'user1']
        self.assertEqual(len(user1_posts), 1)
        self.assertEqual(user1_posts[0]['name'], "User1's Challenge")

        # User2 should see all posts in university feed
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'university'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        # Find User1's post in the university feed
        user1_posts = [c for c in data['ongoing_challenges'] if c['username'] == 'user1']
        self.assertEqual(len(user1_posts), 1)
        self.assertEqual(user1_posts[0]['name'], "User1's Challenge")

        # User3 should see all posts in university feed despite not being friends
        self.client.login(username='user3', password='testpass123')
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'university'})
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        # Find User1's post in the university feed
        user1_posts = [c for c in data['ongoing_challenges'] if c['username'] == 'user1']
        self.assertEqual(len(user1_posts), 1)
        self.assertEqual(user1_posts[0]['name'], "User1's Challenge")
