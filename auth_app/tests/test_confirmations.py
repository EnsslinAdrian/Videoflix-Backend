from django.urls import reverse
from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

class ConfirmationsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="Testpass123!",
            is_active=False 
        )
        self.verify_url = reverse('verify_email')
        self.password_reset_url = reverse('password_reset_request')
        self.password_reset_confirm_url = reverse('password_reset_confirm')

    def test_email_verification_link_invalid(self):
        response = self.client.get(self.verify_url, {'token': 'fake-token'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('invalid', response.json()['message'].lower())

    def test_password_reset_request(self):
        response = self.client.post(self.password_reset_url, {'email': self.user.email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Reset your Password', mail.outbox[0].subject)

    def test_password_reset_request_invalid_email(self):
        response = self.client.post(self.password_reset_url, {'email': 'doesnotexist@example.com'})
        self.assertEqual(response.status_code, 400)

    def test_password_reset_confirm_valid(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        response = self.client.post(self.password_reset_confirm_url, {
            'uid': uid,
            'token': token,
            'new_password': 'NewPassw0rd!'
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassw0rd!'))

    def test_password_reset_confirm_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        response = self.client.post(self.password_reset_confirm_url, {
            'uid': uid,
            'token': 'invalid-token',
            'new_password': 'AnotherPassw0rd!'
        })
        self.assertEqual(response.status_code, 400)
