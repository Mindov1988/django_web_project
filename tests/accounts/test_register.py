from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class LoginViewTests(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'securepassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('login'), data={
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), data={
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_empty(self):
        response = self.client.post(reverse('login'), data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
