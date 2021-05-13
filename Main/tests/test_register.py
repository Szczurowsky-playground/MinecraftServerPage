from django.test import TestCase
from ..models import User
from ..forms import RegisterValidate


class RegisterTestCase(TestCase):
    def test_register(self):
        # Correct registration
        form_data = {'username': 'admin', 'nickname': 'admin', 'email': 'email@email.com', 'password': 'TestCase33.',
                     'password2': 'TestCase33.', 'tos': True}
        form = RegisterValidate(form_data)
        self.assertEqual(form.is_valid(), True)
        # Not safe password
        form_data = {'username': 'admin', 'nickname': 'admin', 'email': 'email@email.com', 'password': 'qwerty',
                     'password2': 'qwerty.', 'tos': True}
        form = RegisterValidate(form_data)
        self.assertEqual(form.is_valid(), False)
        # Not same passwords
        form_data = {'username': 'admin', 'nickname': 'admin', 'email': 'email@email.com', 'password': 'qwerty',
                     'password2': 'qwerty1.', 'tos': True}
        form = RegisterValidate(form_data)
        self.assertEqual(form.is_valid(), False)
        # Not correct username
        form_data = {'username': '''" or ""="''', 'nickname': 'admin', 'email': 'email@email.com', 'password': 'qwerty',
                     'password2': 'qwerty.', 'tos': True}
        form = RegisterValidate(form_data)
        self.assertEqual(form.is_valid(), False)
        # Claimed username
        password = 'sjkk25nk253k'
        admin = User.objects.create(username='admin', email='test@case.com', nickname='Test')
        admin.set_password(password)
        admin.save()
        form_data = {'username': 'admin', 'nickname': 'admin', 'email': 'email@email.com', 'password': 'TestCase33.',
                     'password2': 'TestCase33.', 'tos': True}
        form = RegisterValidate(form_data)
        self.assertEqual(form.is_valid(), False)
        # Claimed nickname
        form_data = {'username': 'admin1', 'nickname': 'Test', 'email': 'email@email.com', 'password': 'TestCase33.',
                     'password2': 'TestCase33.', 'tos': True}
        form = RegisterValidate(form_data)
        self.assertEqual(form.is_valid(), False)
        # Claimed email
        form_data = {'username': 'admin1', 'nickname': 'Test1', 'email': 'test@case.com', 'password': 'TestCase33.',
                     'password2': 'TestCase33.', 'tos': True}
        form = RegisterValidate(form_data)
        self.assertEqual(form.is_valid(), False)
