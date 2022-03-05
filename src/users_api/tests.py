from django.test import TestCase, Client
from .models import User
from django.contrib.auth.models import Permission, Group


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
           User.objects.create_superuser(email='super@mail.com', password='123', is_staff=False, is_active=True)

    def test_staff_user_can_login_admin_page(self):
        staff_user = User.objects.create_superuser(email='staff@mail.com', password='123', is_staff=True, is_active=True)
        client = Client()
        client.login(username=staff_user.email, password=staff_user.password)
        login_page = '/admin/'
        response = client.get(login_page)
        self.assertEqual(response.status_code, 302)

    #temporary, we need to figure out a better way
    def test_staff_user_cannot_delete_superuser(self):
        staff_user = User.objects.create_superuser(email='staff@mail.com', password='123', is_staff=True, is_active=True)
        client = Client()
        client.login(username=staff_user.email, password=staff_user.password)
        login_page = '/admin/'
        response = client.get(login_page)
        self.assertEqual(response.status_code, 302)
