from django.test import TestCase
from ..models import User
from ..forms import LoginValidate


class LoginTestCase(TestCase):
    def test_login(self):
        # Correct
        password = 'sjkk25nk253k'
        admin = User.objects.create(username='admin', email='test@case.com', nickname='Test')
        admin.set_password(password)
        admin.save()
        form_data = {'username': 'admin', 'password': password}
        form = LoginValidate(data=form_data)
        self.assertEqual(form.is_valid(), True)
        # Empty
        form_data = {'username': '', 'password': ''}
        form = LoginValidate(data=form_data)
        self.assertEqual(form.is_valid(), False)
        # No username
        form_data = {'username': '', 'password': password}
        form = LoginValidate(data=form_data)
        self.assertEqual(form.is_valid(), False)
        # No password
        form_data = {'username': 'admin', 'password': ''}
        form = LoginValidate(data=form_data)
        self.assertEqual(form.is_valid(), False)
        # SLQ Injection #1
        form_data = {'username': 'admin', 'password': '105 OR 1=1'}
        form = LoginValidate(data=form_data)
        self.assertEqual(form.is_valid(), False)
        # SLQ Injection #2
        form_data = {'username': 'admin', 'password': '''" or ""="'''}
        form = LoginValidate(data=form_data)
        self.assertEqual(form.is_valid(), False)
