from django.test import TestCase
from accounts.forms import SignUpForm

class SignUpFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'email': 'test@example.com',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'password1': 'StrongPass123!',
            'password2': 'WrongPass123!',
            'email': 'test@example.com',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
