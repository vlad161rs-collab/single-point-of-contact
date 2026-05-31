from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse


from .models import UserRegistrationRequest


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class AuthRegistrationViewsTest(TestCase):
    def test_login_post_with_valid_credentials_redirects(self):
        User.objects.create_user(username='admin', password='admin123')

        response = self.client.post(
            reverse('login'),
            {'username': 'admin', 'password': 'admin123'},
        )

        self.assertEqual(response.status_code, 302)

    def test_register_post_creates_pending_request(self):
        response = self.client.post(
            reverse('portal:register'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'first_name': 'New',
                'last_name': 'User',
                'phone': '',
                'department': '',
                'position': '',
                'requested_role': 'user',
                'password1': 'strongpass123',
                'password2': 'strongpass123',
            },
        )

        self.assertRedirects(response, reverse('portal:register_success'))
        self.assertTrue(
            UserRegistrationRequest.objects.filter(
                username='newuser',
                status='pending',
            ).exists()
        )
