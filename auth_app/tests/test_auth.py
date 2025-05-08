from rest_framework.test import APITestCase
from django.urls import reverse
from auth_app.models import CustomUser

class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.logout_url = reverse('logout')
        self.me_url = reverse('me_user')

        self.user_data = {
            "email": "testuser@example.com",
            "password": "SecurePass123!",
            "first_name": "Test",
            "last_name": "User"
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(CustomUser.objects.filter(email=self.user_data['email']).exists())

    def test_login_user(self):
        CustomUser.objects.create_user(email=self.user_data['email'], password=self.user_data['password'], is_active=True)

        response = self.client.post(self.login_url, {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_logout(self):
        user = CustomUser.objects.create_user(email=self.user_data['email'], password=self.user_data['password'], is_active=True)

        response = self.client.post(self.login_url, {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        })

        self.client.cookies['refresh_token'] = response.cookies['refresh_token'].value

        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.data['message'], "Successfully logged out")

    def test_auth_status_false(self):
        response = self.client.get(reverse('auth_status')) 
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['authenticated'])
