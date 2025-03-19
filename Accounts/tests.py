from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, FriendRequests, Friends
from .forms import SignUpForm,ProfileUpdateForm
from django.urls import reverse
from Garden.models import garden,gardenSquare
from django.conf import settings
# model test
class ProfileModelTest(TestCase):
    def setUp(self):
        """Set up test data for Profile model"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_str_method(self):
        """Test the __str__ method of Profile model"""
        self.assertEqual(str(self.profile), "testuser")

    def test_profile_defaults(self):
        """Test default values for blank fields"""
        user2 = User.objects.create_user(username='user2', password='password123')
        profile2 = Profile.objects.get(user=user2)

        self.assertEqual(profile2.bio, '')
        self.assertEqual(profile2.first_name, "")
        self.assertEqual(profile2.last_name, "")
        self.assertIsNone(profile2.profile_picture)

# forms tests

class testSignupForm(TestCase):
    def test_valid_signup_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'john.doe@gmail.com',
            'password1': 'P@ssword123',
            'password2': 'P@ssword123'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_signup_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'invalid_email',
            'password1': 'P@ssword123',
            'password2': 'P@ssword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])
    def test_non_matching_passwords_signup_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'P@ssword123',
            'password2': 'P@ssword1234'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])
    def test_valid_signup_form_write(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'P@ssword123',
            'password2': 'P@ssword123'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@gmail.com')
        profile = Profile.objects.get(user=user)
        print("FIRST NAME : "+profile.first_name)
        self.assertEqual(profile.first_name, 'John')
        self.assertEqual(profile.last_name, 'Doe')
    def test_garden_creation(self):
        '''
        Test that a garden is created for a user when they sign up
        '''
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1':'P@ssword123',
            'password2':'P@ssword123'
        }
        # form = SignUpForm(data = form_data)
        # user = form.save()
        response = self.client.post('/accounts/signup/', form_data)

        # g = garden.objects.get(user.username=user)
        user=User.objects.get(username='testuser')
        g = garden.objects.get(userID=user)
        self.assertEqual(g.userID, user)
        squares = gardenSquare.objects.filter(gardenID=g)
        self.assertEqual(len(squares), g.size*g.size)
        self.assertEqual(g.size, settings.GARDEN_SIZE)



class testProfileForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = Profile.objects.get(user=self.user)
    def test_valid_profile_form(self):
        form_data = {
            'bio': 'This is a test bio.',
            'profile_picture': 'test.jpg'
        }
        form = ProfileUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
    def test_valid_profile_form_write(self):
        form_data = {
            'bio': 'This is a test bio.',
            'profile_picture': 'test.jpg'
        }
        form = ProfileUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.profile.bio = form.cleaned_data['bio']
        self.profile.profile_picture = form.cleaned_data['profile_picture']
        self.profile.save()
        self.assertEqual(self.profile.bio, 'This is a test bio.')
        self.assertEqual(self.profile.profile_picture, 'test.jpg')

# views tests
class testSignupView(TestCase):
    def test_signup_view(self):
        '''test signup view with a GET request'''
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/signup.html')
    def test_signup_view_post(self):
        '''
        Test the signup view with a POST request
        '''
        response = self.client.post('/accounts/signup/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'P@ssword123',
            'password2':'P@ssword123'
        })
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'Accounts/signup.html')
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)


class LoginTestCase(TestCase):
    def setUp(self):
        """Create a test user"""
        self.username = "testuser"
        self.password = "securepassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_with_correct_credentials(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to success page or render login page
        self.assertTrue(response.wsgi_request.user.is_authenticated) # User should be authenticated

    def test_login_with_incorrect_credentials(self):
        """Test login with incorrect credentials"""
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)  # Login page should re-render with errors
        self.assertFalse(response.wsgi_request.user.is_authenticated) # User should not be authenticated
class LogoutTestCase(TestCase):
    def setUp(self):
        """Create a test user"""
        self.username = "testuser"
        self.password = "securepassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_signout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
class ProfileViewTest(TestCase):
    def setUp(self):
        """Set up a test user and profile"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.profile = Profile.objects.get(user=self.user)

    def test_redirect_if_not_logged_in(self):
        """Test that an unauthenticated user is redirected to the login page"""
        self.client.logout()  # Ensure user is logged out
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(response.url.startswith(reverse('login')))  # Redirects to login page

    def test_get_profile_page(self):
        """Test that an authenticated user can access the profile page"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounts/profile.html')
        self.assertContains(response, self.user.username)  # Ensure the username appears on the page

    def test_post_update_profile(self):
        """Test that a user can update their bio and profile picture"""
        response = self.client.post(reverse('profile'), {
            'bio': 'This is my new bio!',
            'profile_picture': 'new_picture.jpg'
        })

        # Refresh the profile from the database
        self.profile.refresh_from_db()

        self.assertEqual(response.status_code, 302)  # Should redirect back to profile page
        self.assertEqual(self.profile.bio, 'This is my new bio!')
        self.assertEqual(self.profile.profile_picture, 'new_picture.jpg')

    def test_post_update_profile_without_picture(self):
        """Test profile update when profile picture is not provided"""
        response = self.client.post(reverse('profile'), {
            'bio': 'Updated bio without picture'
        })

        self.profile.refresh_from_db()

        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.assertEqual(self.profile.bio, 'Updated bio without picture')
        self.assertIsNone(self.profile.profile_picture)  # Should remain None if not updated

#Test class to test the functionality of creating friends in the DB
class FriendsTest(TestCase):
    def setUp(self):
        #Set up 2 users for the tests
        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")

    #Testing when friendship is created
    def testCreateFriendship(self):
        #Creating a friendship between the two users
        friendship = Friends.objects.create(userID1=self.user1, userID2=self.user2)
        self.assertEqual(friendship.userID1, self.user1)
        self.assertEqual(friendship.userID2, self.user2)

    #Testing that a duplicate friendship is not allowed
    def testDuplicateFriendship(self):
        Friends.objects.create(userID1=self.user1, userID2=self.user2)
        with self.assertRaises(Exception):
            Friends.objects.create(userID1=self.user1, userID2=self.user2)

    #Testing the Str method works properly
    def testStr(self):
        friendship = Friends.objects.create(userID1=self.user1, userID2=self.user2)
        self.assertEqual(str(friendship), "user1 is friends with user2")


#Test class for friend request table in the DB
class FriendRequestsTest(TestCase):
    #Set up the two users needed for the requests to work
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")

    #Create a request and make sure it works
    def testCreateFriendRequest(self):
        request = FriendRequests.objects.create(senderID=self.user1, receiverID=self.user2)
        self.assertEqual(request.senderID, self.user1)
        self.assertEqual(request.receiverID, self.user2)

    #Make sure that no duplicate friend requests are allowed
    def testDuplicateFriendRequest(self):
        FriendRequests.objects.create(senderID=self.user1, receiverID=self.user2)
        with self.assertRaises(Exception):
            FriendRequests.objects.create(senderID=self.user1, receiverID=self.user2)

    #Test to make sure the STR method works properly
    def testStr(self):
        request = FriendRequests.objects.create(senderID=self.user1, receiverID=self.user2)
        self.assertEqual(str(request), "user1 sent a request to user2")


class DeleteAccountViewTest(TestCase):
    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_delete_account_authenticated_user(self):
        """Ensure a logged-in user can delete their account."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("delete_account"))

        # Check user is deleted
        self.assertFalse(User.objects.filter(username="testuser").exists())

        # Check redirection
        self.assertRedirects(response, "/")

        # Check success message
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your account has been deleted successfully.")

    def test_delete_account_unauthenticated_user(self):
        """Ensure an unauthenticated user is redirected to login."""
        response = self.client.post(reverse("delete_account"))

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))
