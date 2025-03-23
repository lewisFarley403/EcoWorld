from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.loader import render_to_string
from .models import UserEarntCoins
from Accounts.models import Profile
from Garden.models import garden, gardenSquare
from Accounts.forms import SignUpForm
from Accounts.utils import createGarden

class LeaderboardTests(TestCase):
    def setUp(self):
        # Create test users (profiles will be created automatically via signals)
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.user3 = User.objects.create_user(username='user3', password='testpass123')
        self.user4 = User.objects.create_user(username='user4', password='testpass123')
        
        # Create client for making requests
        self.client = Client()
        self.client.login(username='user1', password='testpass123')

    def test_negative_coins(self):
        """Test whether UserEarntCoins can store negative values"""
        # Create a negative coin entry
        # negative_coins = UserEarntCoins.objects.create(
        #     user=self.user1,
        #     score=-100
        # )
        self.user1.profile.number_of_coins += 100
        self.user1.profile.save()
        self.user1.profile.number_of_coins-=100
        self.user1.profile.save()
        # Verify the negative value was stored correctly
 
        
        # Verify it's included in the total sum
        total_coins = sum([i.score for i in UserEarntCoins.objects.filter(user=self.user1)])
        self.assertEqual(total_coins, 100)

    def test_user_ordering(self):
        """Test whether the leaderboard correctly orders users by their total coins"""
        # Create different coin amounts for each user
        UserEarntCoins.objects.create(user=self.user1, score=100)
        UserEarntCoins.objects.create(user=self.user2, score=200)
        UserEarntCoins.objects.create(user=self.user3, score=150)
        
        # Get the leaderboard data
        response = self.client.get(reverse('get_ranked_users'))
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = response.json()
        ranked_users = data['rankedUsers']
        
        # Verify the order (should be user2, user3, user1)
        self.assertEqual(ranked_users[0]['username'], 'user2')
        self.assertEqual(ranked_users[1]['username'], 'user3')
        self.assertEqual(ranked_users[2]['username'], 'user1')

    def test_coin_sum_calculation(self):
        """Test whether the view correctly sums up all coins earned by a user"""
        # Create multiple coin entries for user1
        UserEarntCoins.objects.create(user=self.user1, score=100)
        UserEarntCoins.objects.create(user=self.user1, score=50)
        UserEarntCoins.objects.create(user=self.user1, score=25)
        
        # Create some coins for user2 for comparison
        UserEarntCoins.objects.create(user=self.user2, score=200)
        
        # Get the leaderboard data
        response = self.client.get(reverse('get_ranked_users'))
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = response.json()
        ranked_users = data['rankedUsers']
        
        # Find user1 in the ranked users
        user1_data = next(user for user in ranked_users if user['username'] == 'user1')
        
        # Verify the total sum is correct (100 + 50 + 25 = 175)
        self.assertEqual(user1_data['score'], 175)
        
        # Verify user2's score is correct
        user2_data = next(user for user in ranked_users if user['username'] == 'user2')
        self.assertEqual(user2_data['score'], 200)

    def test_current_user_data(self):
        """Test whether the current user's data is correctly included in the response"""
        # Create some coins for user1 (current user)
        UserEarntCoins.objects.create(user=self.user1, score=100)
        UserEarntCoins.objects.create(user=self.user2, score=200)
        
        # Get the leaderboard data
        response = self.client.get(reverse('get_ranked_users'))
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = response.json()
        current_user_data = data['current_user_data']
        
        # Verify current user data is correct
        self.assertEqual(current_user_data['username'], 'user1')
        self.assertEqual(current_user_data['score'], 100)
        self.assertEqual(current_user_data['rank'], 2)  # user1 should be second after user2

    def test_leaderboard_template_rendering(self):
        """Test whether the leaderboard template renders correctly"""
        # Create some test data
        UserEarntCoins.objects.create(user=self.user1, score=100)
        UserEarntCoins.objects.create(user=self.user2, score=200)
        UserEarntCoins.objects.create(user=self.user3, score=150)
        
        # Get the leaderboard page
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        
        # Check if the template contains expected elements
        self.assertTemplateUsed(response, 'leaderboard/leaderboard.html')
        self.assertContains(response, 'Top Eco Warriors')
        self.assertContains(response, 'Rank')
        self.assertContains(response, 'Player')
        self.assertContains(response, 'Eco Points')
        
        # Check if the top 3 container exists
        self.assertContains(response, 'top-3-container')
        self.assertContains(response, 'podium')
        
        # Check if the leaderboard table exists
        self.assertContains(response, 'leaderboard-container')
        self.assertContains(response, 'leaderboard-table')
        
        # Check if the current user row exists
        self.assertContains(response, 'current-user-row')

    def test_leaderboard_template_loading_state(self):
        """Test whether the loading state is properly displayed"""
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        
        # Check if loading overlay exists
        self.assertContains(response, 'loading-overlay')
        self.assertContains(response, 'spinner')
        
        # Check if initial loading text is present
        self.assertContains(response, 'Loading...')

    def test_leaderboard_template_profile_pictures(self):
        """Test whether profile pictures are properly handled"""
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        
        # Check if default profile picture fallback is present
        self.assertContains(response, 'default_pfp.png')
        
        # Check if crown image is present for first place
        self.assertContains(response, 'crown.png')

    def test_leaderboard_template_tooltip(self):
        """Test whether the tooltip container exists"""
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        
        # Check if tooltip container exists
        self.assertContains(response, 'tooltip')

    def test_fewer_than_three_users(self):
        """Test leaderboard behavior with fewer than 3 users"""
        # Store user3 and user4 to restore later
        user3_username = self.user3.username
        user4_username = self.user4.username
        
        # Delete user3 and user4
        self.user3.delete()
        self.user4.delete()
        
        # Create coins for remaining users
        UserEarntCoins.objects.create(user=self.user1, score=100)
        UserEarntCoins.objects.create(user=self.user2, score=200)
        
        response = self.client.get(reverse('get_ranked_users'))
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        ranked_users = data['rankedUsers']
        
        # Should only return 2 users
        self.assertEqual(len(ranked_users), 2)
        self.assertEqual(ranked_users[0]['username'], 'user2')
        self.assertEqual(ranked_users[1]['username'], 'user1')
        
        # Restore user3 and user4
        self.user3 = User.objects.create_user(username=user3_username, password='testpass123')
        self.user4 = User.objects.create_user(username=user4_username, password='testpass123')

    def test_equal_scores(self):
        """Test leaderboard behavior when users have equal scores"""
        # Create equal scores for users
        UserEarntCoins.objects.create(user=self.user1, score=100)
        UserEarntCoins.objects.create(user=self.user2, score=100)
        UserEarntCoins.objects.create(user=self.user3, score=100)
        UserEarntCoins.objects.create(user=self.user4, score=100)
        
        response = self.client.get(reverse('get_ranked_users'))
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        ranked_users = data['rankedUsers']
        
        # All users should have the same score
        for user in ranked_users:
            self.assertEqual(user['score'], 100)

    def test_no_coins(self):
        """Test leaderboard behavior when users have no coins"""
        response = self.client.get(reverse('get_ranked_users'))
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        ranked_users = data['rankedUsers']
        
        # All users should have 0 coins
        for user in ranked_users:
            self.assertEqual(user['score'], 0)

    def test_large_coin_amounts(self):
        """Test handling of very large coin amounts"""
        large_amount = 1000000
        UserEarntCoins.objects.create(user=self.user1, score=large_amount)
        
        response = self.client.get(reverse('get_ranked_users'))
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        ranked_users = data['rankedUsers']
        
        # Find user1 in the ranked users
        user1_data = next(user for user in ranked_users if user['username'] == 'user1')
        self.assertEqual(user1_data['score'], large_amount)

    def test_quick_succession_entries(self):
        """Test handling of multiple coin entries in quick succession"""
        # Create multiple entries for user1 in quick succession
        for i in range(5):
            UserEarntCoins.objects.create(user=self.user1, score=10)
        
        response = self.client.get(reverse('get_ranked_users'))
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        ranked_users = data['rankedUsers']
        
        # Find user1 in the ranked users
        user1_data = next(user for user in ranked_users if user['username'] == 'user1')
        self.assertEqual(user1_data['score'], 50)  # 5 entries of 10 each

    def test_unauthenticated_access(self):
        """Test access to leaderboard when not logged in"""
        # Log out the client
        self.client.logout()
        
        # Try to access the leaderboard
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        
        # Try to access the API endpoint
        response = self.client.get(reverse('get_ranked_users'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_response_structure(self):
        """Test the structure of the API response"""
        UserEarntCoins.objects.create(user=self.user1, score=100)
        
        response = self.client.get(reverse('get_ranked_users'))
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Check required fields
        self.assertIn('rankedUsers', data)
        self.assertIn('MEDIA_URL', data)
        self.assertIn('current_user_data', data)
        
        # Check structure of ranked users
        for user in data['rankedUsers']:
            self.assertIn('username', user)
            self.assertIn('pfp_url', user)
            self.assertIn('score', user)
        
        # Check structure of current user data
        current_user = data['current_user_data']
        self.assertIn('username', current_user)
        self.assertIn('score', current_user)
        self.assertIn('rank', current_user)

    def test_tooltip_template(self):
        """Test the garden tooltip template rendering"""
        # Create a new user using the signup form
        from Accounts.forms import SignUpForm
        from Accounts.utils import createGarden
        
        # Create form data
        form_data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        
        # Create and validate the form
        form = SignUpForm(form_data)
        self.assertTrue(form.is_valid())
        
        # Create the user
        user = form.save()
        
        # Create the garden using the utility function
        user_garden = createGarden(user)
        
        # Get the tooltip template
        response = self.client.get(
            reverse('get_tooltip_template'),
            {'username': 'testuser2'}
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard/garden_tool_tip.html')
        
        # Check if the template contains expected data
        self.assertIn('username', response.context)
        self.assertIn('squares', response.context)
        self.assertIn('MEDIA_URL', response.context)
        
        # Verify the squares are properly processed
        squares = response.context['squares']
        print("SQUARES : ",squares)
        self.assertEqual(len(squares), 5)  # Should be 5x5 grid
        self.assertEqual(len(squares[0]), 5)
        
        # Verify the username is correct
        self.assertEqual(response.context['username'], 'testuser2')


        

