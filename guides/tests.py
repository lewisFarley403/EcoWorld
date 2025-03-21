from importlib.resources import contents

from django.template.defaultfilters import title
from django.test import TestCase
from django.contrib.auth.models import User

from .forms import GuidesForm
from .models import ContentQuizPair,UserQuizResult
from Accounts.models import Profile
# Create your tests here.

class ContentQuizPairModelTest(TestCase):
    def setUp(self):
        self.guide1 = ContentQuizPair.objects.create(title='test1',
                                                     content= 'test content',
                                                     quiz_questions='',
                                                     )

    def test_contentQuizPair_str_method(self):
        self.assertEqual(str(self.guide1),'test1')


    def test_contentQuizPair_defaults(self):
        contentQuizPair2 = ContentQuizPair.objects.create(title='title',
                                                          content='content',
                                                          quiz_questions = ''
                                                          )
        self.assertEqual(contentQuizPair2.quiz_max_marks,-1)
        self.assertEqual(contentQuizPair2.reward,50)

    def test_contentQuizPair_custom_values(self):
        contentQuizPair3 = ContentQuizPair.objects.create(title='custom_title',
                                                          content='custom_content',
                                                          quiz_questions='',
                                                          quiz_max_marks=10,
                                                          reward=100
        )
        self.assertEqual(contentQuizPair3.quiz_max_marks, 10)
        self.assertEqual(contentQuizPair3.reward, 100)


class UserQuizResultsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.guide1 = ContentQuizPair.objects.create(
            title='test guide 1',
            content='test content',
            quiz_questions='',
            quiz_max_marks=1,
            reward=50
        )
        self.profile1 = Profile.objects.get(user=self.user)
        self.profile1Results = UserQuizResult(
            user=self.user,
            content_quiz_pair=self.guide1
        )

    def test_userQuizResults_defaults(self):
        self.assertEqual(self.profile1Results.score, 0)
        self.assertEqual(self.profile1Results.best_result, 0)
        self.assertEqual(self.profile1Results.previous_best, 0)
        self.assertEqual(self.profile1Results.is_completed, False)

    def test_userQuizResults_str_method(self):
        self.assertEqual(str(self.profile1Results), "testuser - test guide 1")

    def test_userQuizResults_save_method(self):
        result = UserQuizResult.objects.create(
            user=self.user,
            content_quiz_pair=self.guide1,
            score=1,
            best_result=1,
            previous_best=0
        )
        result.save()
        self.assertTrue(result.is_completed)

    def test_userQuizResults_update_best_result(self):
        result = UserQuizResult.objects.create(
            user=self.user,
            content_quiz_pair=self.guide1,
            score=0,
            best_result=0,
            previous_best=0
        )
        result.score = 1
        result.best_result = 1
        result.save()
        self.assertEqual(result.best_result, 1)
        self.assertEqual(result.previous_best, 0)

    def test_userQuizResults_previous_best_update(self):
        result = UserQuizResult.objects.create(
            user=self.user,
            content_quiz_pair=self.guide1,
            score=1,
            best_result=1,
            previous_best=1
        )
        result.score = 0
        result.save()
        self.assertEqual(result.previous_best, 1)
        self.assertEqual(result.best_result, 1)

class TestGuidesForm(TestCase):
    def test_valid_guides_form(self):
        form_data = {
            'title': 'Test Guide',
            'content': 'This is a test guide content.'
        }
        form = GuidesForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_guides_form(self):
        form_data = {
            'title': '',  # Title is required
            'content': 'This is a test guide content.'
        }
        form = GuidesForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

from django.urls import reverse

class GuidesViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.guide1 = ContentQuizPair.objects.create(
            title='test guide 1',
            content='test content',
            quiz_questions='',
            quiz_max_marks=1,
            reward=50
        )

    def test_menu_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test guide 1')

    def test_content_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('content', args=[self.guide1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test content')
