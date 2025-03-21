from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from EcoWorld.models import challenge, card, ongoingChallenge, cardRarity
from Accounts.models import Friends
from .models import Post, PostInteraction
import json


class PostCreationTest(TestCase):
    """Test post creation for various submission types
    
    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a card rarity for test cards
        self.card_rarity = cardRarity.objects.create(title="Common")
        
        # Create test challenge and card
        self.challenge_obj = challenge.objects.create(
            name='Test Challenge',
            description='Test description',
            redirect_url='http://example.com',
            created_on=timezone.now()
        )
        
        self.card_obj = card.objects.create(
            title='Test Card',
            description='Test card description',
            rarity=self.card_rarity,
            image='cards/test.png'
        )
        
        # Create a client and log in
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
    
    def test_challenge_post_creation(self):
        """Test that a post is created when a challenge is completed
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Create an ongoing challenge
        ongoing_challenge = ongoingChallenge.objects.create(
            user=self.user,
            challenge=self.challenge_obj,
            submission='Test submission'
        )
        
        # Create post from ongoing challenge
        post = Post.create_from_ongoing_challenge(ongoing_challenge)
        
        # Verify post was created properly
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.post_type, 'challenge')
        self.assertEqual(post.challenge, self.challenge_obj)
        self.assertEqual(post.submission, 'Test submission')
    
    def test_card_post_creation(self):
        """Test that a post is created when a card is earned
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Create post from card
        post = Post.create_from_card(self.card_obj, self.user)
        
        # Verify post was created properly
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.post_type, 'card')
        self.assertEqual(post.card_achievement, self.card_obj)
    
    def test_guide_post_creation(self):
        """Test that a post is created when a guide is completed
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Create post from guide
        post = Post.create_from_guide('Test Guide', 'Guide description', self.user, 90)
        
        # Verify post was created properly
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.post_type, 'guide')
        self.assertEqual(post.title, 'Test Guide')
        self.assertEqual(post.description, 'Guide description')
        self.assertEqual(post.score, 90)


class FeedDisplayTest(TestCase):
    """Test the feed display with various filters and conditions
    
    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.user3 = User.objects.create_user(username='user3', password='password')
        
        # Create a card rarity for test cards
        self.card_rarity = cardRarity.objects.create(title="Common")
        
        # Create test challenge and card
        self.challenge_obj = challenge.objects.create(
            name='Test Challenge',
            description='Test description',
            created_on=timezone.now()
        )
        
        self.card_obj = card.objects.create(
            title='Test Card',
            description='Test card description',
            rarity=self.card_rarity,
            image='cards/test.png'
        )
        
        # Create posts for users
        self.user1_post1 = Post.objects.create(
            user=self.user1,
            post_type='challenge',
            challenge=self.challenge_obj,
            submission='User 1 submission'
        )
        
        self.user1_post2 = Post.objects.create(
            user=self.user1,
            post_type='card',
            card_achievement=self.card_obj
        )
        
        self.user2_post = Post.objects.create(
            user=self.user2,
            post_type='guide',
            title='Test Guide',
            description='Test guide description',
            score=85
        )
        
        self.user3_post = Post.objects.create(
            user=self.user3,
            post_type='challenge',
            challenge=self.challenge_obj,
            submission='User 3 submission'
        )
        
        # Create friendships
        Friends.objects.create(userID1=self.user1, userID2=self.user2)
        
        # Create a client
        self.client = Client()
    
    def test_empty_my_posts(self):
        """Test that appropriate message is shown when user has no posts
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Create a new user with no posts
        empty_user = User.objects.create_user(username='emptyuser', password='password')
        self.client.login(username='emptyuser', password='password')
        
        # Get 'my' filter
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'my'})
        data = json.loads(response.content)
        
        # Verify empty lists
        self.assertEqual(len(data['ongoing_challenges']), 0)
        self.assertEqual(len(data['card_achievements']), 0)
        self.assertEqual(len(data['guides']), 0)
    
    def test_no_friends_message(self):
        """Test that appropriate message is shown when user has no friends
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Create a new user with no friends
        lonely_user = User.objects.create_user(username='lonelyuser', password='password')
        self.client.login(username='lonelyuser', password='password')
        
        # Get 'friends' filter
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'friends'})
        data = json.loads(response.content)
        
        # Verify has_no_friends flag is set
        self.assertTrue(data['has_no_friends'])
    
    def test_my_posts_filter(self):
        """Test that 'my' filter only shows current user's posts
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        self.client.login(username='user1', password='password')
        
        # Get 'my' filter
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'my'})
        data = json.loads(response.content)
        
        # Verify only user1's posts are returned
        self.assertEqual(len(data['ongoing_challenges']), 1)
        self.assertEqual(len(data['card_achievements']), 1)
        self.assertEqual(data['ongoing_challenges'][0]['username'], 'user1')
        self.assertEqual(data['card_achievements'][0]['username'], 'user1')
    
    def test_all_my_posts_shown(self):
        """Test that all of the current user's posts are shown in 'my' filter
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        self.client.login(username='user1', password='password')
        
        # Get 'my' filter
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'my'})
        data = json.loads(response.content)
        
        # Verify all user1's posts are returned (1 challenge and 1 card)
        self.assertEqual(len(data['ongoing_challenges']), 1)
        self.assertEqual(len(data['card_achievements']), 1)
    
    def test_friends_filter(self):
        """Test that 'friends' filter shows only friends' posts
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        self.client.login(username='user1', password='password')
        
        # Get 'friends' filter
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'friends'})
        data = json.loads(response.content)
        
        # Verify only user2's posts are returned (user2 is a friend of user1)
        self.assertEqual(len(data['guides']), 1)
        self.assertEqual(data['guides'][0]['username'], 'user2')
        
        # Verify user3's posts are not shown (not a friend of user1)
        for challenge in data['ongoing_challenges']:
            self.assertNotEqual(challenge['username'], 'user3')
    
    def test_university_filter(self):
        """Test that 'university' filter shows all posts
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        self.client.login(username='user1', password='password')
        
        # Make API request with filter=university
        # Since the view does not explicitly implement 'university' filter,
        # it will show all posts by default when not 'my' or 'friends'
        response = self.client.get(reverse('forum:get_challenge_info'), {'filter': 'university'})
        data = json.loads(response.content)
        # print('data : ',data)
        
        # Count posts in the response
        total_posts = len(data['ongoing_challenges']) + len(data['card_achievements']) + len(data['guides'])
        
        # Should be 4 posts total (2 from user1, 1 from user2, 1 from user3)
        self.assertEqual(total_posts, 4)
        
        # Check for posts from different users
        user_names = set()
        for post in data['ongoing_challenges']:
            user_names.add(post['username'])
        for post in data['card_achievements']:
            user_names.add(post['username'])
        for post in data['guides']:
            user_names.add(post['username'])
        
        # Should contain posts from all three users
        self.assertEqual(len(user_names), 3)
        self.assertIn('user1', user_names)
        self.assertIn('user2', user_names)
        self.assertIn('user3', user_names)


class PostSortingTest(TestCase):
    """Test post sorting functionality
    
    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    
    def setUp(self):
        # Create test user and posts
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.challenge_obj = challenge.objects.create(
            name='Test Challenge',
            description='Test description',
            created_on=timezone.now()
        )
        
        # Create posts with different timestamps
        import datetime
        
        self.post1 = Post.objects.create(
            user=self.user,
            post_type='challenge',
            challenge=self.challenge_obj,
            created_at=timezone.now() - datetime.timedelta(days=2)
        )
        
        self.post2 = Post.objects.create(
            user=self.user,
            post_type='challenge',
            challenge=self.challenge_obj,
            created_at=timezone.now() - datetime.timedelta(days=1)
        )
        
        self.post3 = Post.objects.create(
            user=self.user,
            post_type='challenge',
            challenge=self.challenge_obj,
            created_at=timezone.now()
        )
        
        # Add likes to posts
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.user3 = User.objects.create_user(username='user3', password='password')
        
        # Post3: 2 likes
        PostInteraction.objects.create(user=self.user, post=self.post3, interaction_type='like')
        PostInteraction.objects.create(user=self.user2, post=self.post3, interaction_type='like')
        
        # Post1: 3 likes
        PostInteraction.objects.create(user=self.user, post=self.post1, interaction_type='like')
        PostInteraction.objects.create(user=self.user2, post=self.post1, interaction_type='like')
        PostInteraction.objects.create(user=self.user3, post=self.post1, interaction_type='like')
        
        # Post2: 1 like
        PostInteraction.objects.create(user=self.user, post=self.post2, interaction_type='like')
        
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
    
    def test_sort_by_recent(self):
        """Test that posts are sorted by most recent
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Since the posts have different created_at timestamps, and the Post model has
        # ordering = ['-created_at'] in Meta, they should already be sorted by most recent
        posts = Post.objects.all()
        
        # Most recent first
        self.assertEqual(posts[0], self.post3)
        self.assertEqual(posts[1], self.post2)
        self.assertEqual(posts[2], self.post1)
    
    def test_sort_by_likes(self):
        """Test that posts can be sorted by like count
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Get like counts
        post1_likes = PostInteraction.objects.filter(post=self.post1, interaction_type='like').count()
        post2_likes = PostInteraction.objects.filter(post=self.post2, interaction_type='like').count()
        post3_likes = PostInteraction.objects.filter(post=self.post3, interaction_type='like').count()
        
        # Verify like counts
        self.assertEqual(post1_likes, 3)
        self.assertEqual(post2_likes, 1)
        self.assertEqual(post3_likes, 2)
        
        # Sort posts by like count
        posts_by_likes = Post.objects.annotate(
            like_count=Count('interactions', filter=Q(interactions__interaction_type='like'))
        ).order_by('-like_count')
        
        # Most likes first
        self.assertEqual(posts_by_likes[0], self.post1)  # 3 likes
        self.assertEqual(posts_by_likes[1], self.post3)  # 2 likes
        self.assertEqual(posts_by_likes[2], self.post2)  # 1 like


class PostCreationErrorTest(TestCase):
    """Test error cases for post creation
    
    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
    
    def test_invalid_post_type(self):
        """Test creating a post with invalid post type
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        response = self.client.post(
            reverse('forum:create_post'),
            json.dumps({
                'post_type': 'invalid_type',
                'content_id': 1
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid post type')
    
    def test_invalid_content_id(self):
        """Test creating a post with invalid content_id
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        response = self.client.post(
            reverse('forum:create_post'),
            json.dumps({
                'post_type': 'challenge',
                'content_id': 99999  # Non-existent ID
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


class PostInteractionTest(TestCase):
    """Test post interaction functionality
    
    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        # Create a test post
        self.post = Post.objects.create(
            user=self.user,
            post_type='guide',
            title='Test Post',
            description='Test Description'
        )
    
    def test_remove_interaction(self):
        """Test removing a like/dislike interaction
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # First add a like
        response = self.client.post(
            reverse('forum:interact_with_post'),
            json.dumps({
                'post_id': self.post.id,
                'type': 'like'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Then remove it by clicking like again
        response = self.client.post(
            reverse('forum:interact_with_post'),
            json.dumps({
                'post_id': self.post.id,
                'type': 'like'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['action'], 'removed')
        self.assertEqual(response.json()['likes'], 0)
    
    def test_change_interaction(self):
        """Test changing a like to dislike (and vice versa)
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # First add a like
        response = self.client.post(
            reverse('forum:interact_with_post'),
            json.dumps({
                'post_id': self.post.id,
                'type': 'like'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Then change it to dislike
        response = self.client.post(
            reverse('forum:interact_with_post'),
            json.dumps({
                'post_id': self.post.id,
                'type': 'dislike'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['action'], 'changed')
        self.assertEqual(response.json()['likes'], 0)
        self.assertEqual(response.json()['dislikes'], 1)
    
    def test_get_nonexistent_post_interactions(self):
        """Test getting interactions for non-existent post
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        response = self.client.get(reverse('forum:get_post_interactions', args=[99999]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Post not found')
    
    def test_unique_interaction_constraint(self):
        """Test unique constraint on user-post interaction pairs
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Create first interaction
        PostInteraction.objects.create(
            user=self.user,
            post=self.post,
            interaction_type='like'
        )
        
        # Try to create duplicate interaction
        with self.assertRaises(Exception):
            PostInteraction.objects.create(
                user=self.user,
                post=self.post,
                interaction_type='dislike'
            )


class GamekeeperTest(TestCase):
    """Test gamekeeper functionality
    
    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    
    def setUp(self):
        # Create regular user and gamekeeper
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.user3 = User.objects.create_user(username='user3', password='password')
        
        # Create gamekeeper with required permission
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from Accounts.models import Profile
        
        # Get the permission
        content_type = ContentType.objects.get_for_model(Profile)
        permission = Permission.objects.get(
            codename='can_view_gamekeeper_button',
            content_type=content_type
        )
        
        # Create gamekeeper user with permission
        self.gamekeeper = User.objects.create_user(
            username='gamekeeper',
            password='password',
            is_staff=True
        )
        self.gamekeeper.user_permissions.add(permission)
        
        self.client = Client()
        
        # Create test posts with different interaction ratios
        self.post1 = Post.objects.create(
            user=self.user,
            post_type='guide',
            title='High Dislike Post',
            description='Test Description'
        )
        self.post2 = Post.objects.create(
            user=self.user,
            post_type='guide',
            title='Low Dislike Post',
            description='Test Description'
        )
        
        # Add interactions to post1 (high dislike ratio)
        PostInteraction.objects.create(user=self.user, post=self.post1, interaction_type='like')
        PostInteraction.objects.create(user=self.user2, post=self.post1, interaction_type='dislike')
        PostInteraction.objects.create(user=self.user3, post=self.post1, interaction_type='dislike')
        
        # Add interactions to post2 (low dislike ratio)
        PostInteraction.objects.create(user=self.user, post=self.post2, interaction_type='like')
        PostInteraction.objects.create(user=self.user2, post=self.post2, interaction_type='like')
        PostInteraction.objects.create(user=self.user3, post=self.post2, interaction_type='dislike')
    
    def test_gamekeeper_page_access(self):
        """Test access control for gamekeeper page
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        # Try accessing as regular user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('forum:forum_gamekeeper'))
        self.assertEqual(response.status_code, 302) # Redirects to login page
        
        # Access as gamekeeper
        self.client.login(username='gamekeeper', password='password')
        response = self.client.get(reverse('forum:forum_gamekeeper'))
        self.assertEqual(response.status_code, 200)
    

    
    def test_post_deletion(self):
        """Test post deletion functionality
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        self.client.login(username='gamekeeper', password='password')
        
        # Delete a post
        response = self.client.post(reverse('forum:delete_post', args=[self.post1.id]))
        print('response : ',response)
        self.assertEqual(response.status_code, 302) # Redirects to gamekeeper page
        
        # Verify post is deleted
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())
        # Verify interactions are also deleted
        self.assertFalse(PostInteraction.objects.filter(post_id=self.post1.id).exists())


class ModelTest(TestCase):
    """Test model functionality
    
    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_post_visibility_choices(self):
        """Test Post model's visibility choices
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        post = Post.objects.create(
            user=self.user,
            post_type='guide',
            title='Test Post',
            description='Test Description',
            visibility='friends'
        )
        self.assertEqual(post.visibility, 'friends')
        
        post.visibility = 'university'
        post.save()
        self.assertEqual(post.visibility, 'university')
    
    def test_post_string_representation(self):
        """Test Post model's string representation
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        post = Post.objects.create(
            user=self.user,
            post_type='guide',
            title='Test Post',
            description='Test Description'
        )
        self.assertEqual(str(post), "testuser's guide post")
    
    def test_post_interaction_string_representation(self):
        """Test PostInteraction model's string representation
        
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        post = Post.objects.create(
            user=self.user,
            post_type='guide',
            title='Test Post',
            description='Test Description'
        )
        interaction = PostInteraction.objects.create(
            user=self.user,
            post=post,
            interaction_type='like'
        )
        self.assertEqual(str(interaction), "testuser liked testuser's guide post")
