from django.test import TestCase
from .models import User, CustomUserManager


class Test_Create_User(TestCase):

    def test_user_create(self):
        user = User.objects.create_user(email='testuser@mail.com', password='123')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'testuser@mail.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_superuser)
 

    def test_raises_error_when_no_email(self):
        self.assertRaises(ValueError, User.objects.create_user, email='', password='123')

    def test_superuser_create(self):
        user = User.objects.create_superuser(email='super@mail.com', password='123')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'super@mail.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
 
    def test_superuser_raises_error_when_no_email(self):
       with self.assertRaisesMessage(ValueError, 'Superuser must be assigned to is_staff=True.'):
           User.objects.create_superuser(email='super@mail.com', password='123', is_staff=False)
        