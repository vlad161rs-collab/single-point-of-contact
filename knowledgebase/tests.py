from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Article, Request, Comment
from portal.models import UserProfile, Department, UserRegistrationRequest
from .utils import auto_classify_request, auto_assign_request


class ArticleModelTest(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article",
            content="Test content"
        )

    def test_article_creation(self):
        self.assertEqual(self.article.title, "Test Article")
        self.assertIsNotNone(self.article.pub_date)

    def test_article_str(self):
        self.assertEqual(str(self.article), "Test Article")


class RequestModelTest(TestCase):
    def setUp(self):
        self.request = Request.objects.create(
            title="Test Request",
            description="Test description",
            category="Technical",
            status="New"
        )

    def test_request_creation(self):
        self.assertEqual(self.request.title, "Test Request")
        self.assertEqual(self.request.status, "New")

    def test_request_str(self):
        self.assertEqual(str(self.request), "Test Request")


class AutoClassificationTest(TestCase):
    def test_technical_classification(self):
        category = auto_classify_request(
            "Ошибка в системе",
            "Не работает принтер, выдает ошибку"
        )
        self.assertEqual(category, "Technical")

    def test_content_classification(self):
        category = auto_classify_request(
            "Добавить статью",
            "Нужно добавить новый контент на сайт"
        )
        self.assertEqual(category, "Content")

    def test_unclassified(self):
        category = auto_classify_request(
            "Вопрос",
            "Как дела?"
        )
        self.assertEqual(category, "Uncategorized")


class RequestViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        profile, created = UserProfile.objects.get_or_create(user=self.user)
        if created:
            profile.role = 'user'
            profile.save()

    def test_requests_page_requires_login(self):
        response = self.client.get(reverse('knowledgebase:requests-page'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_requests_page_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('knowledgebase:requests-page'))
        self.assertEqual(response.status_code, 200)

    def test_create_request(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('knowledgebase:requests-page'),
            {
                'title': 'Test Request',
                'description': 'Test description',
                'category': 'Technical'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Request.objects.filter(title='Test Request').exists())


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        self.department = Department.objects.create(name='IT')
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.profile.role = 'moderator'
        self.profile.department = self.department
        self.profile.save()

    def test_profile_creation(self):
        self.assertEqual(self.profile.role, 'moderator')
        self.assertEqual(self.profile.department, self.department)

    def test_profile_is_moderator(self):
        self.assertTrue(self.profile.is_moderator)

    def test_profile_is_not_admin(self):
        self.assertFalse(self.profile.is_admin)


class RegistrationRequestTest(TestCase):
    def setUp(self):
        self.reg_request = UserRegistrationRequest.objects.create(
            username='newuser',
            email='newuser@example.com',
            requested_role='user',
            status='pending'
        )

    def test_registration_request_creation(self):
        self.assertEqual(self.reg_request.status, 'pending')
        self.assertEqual(self.reg_request.requested_role, 'user')

    def test_registration_request_str(self):
        self.assertIn('newuser', str(self.reg_request))


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.article = Article.objects.create(
            title="Test Article",
            content="Content"
        )
        self.comment = Comment.objects.create(
            text="Test comment",
            article=self.article,
            user=self.user
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.text, "Test comment")
        self.assertEqual(self.comment.article, self.article)

    def test_comment_validation(self):
        # Тест валидации - комментарий должен быть привязан к статье или заявке
        invalid_comment = Comment(text="Invalid")
        with self.assertRaises(Exception):
            invalid_comment.clean()
