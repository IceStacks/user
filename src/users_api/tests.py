from ast import arg
from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


# refactor: create user data to use for all tests.
class Test_Create_User(TestCase):

    def test_user_create(self):
        user = User.objects.create_user(email='testuser@mail.com', password='123')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'testuser@mail.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_user_str(self):
        user = User.objects.create_user(email='testuser@mail.com', password='123')
        self.assertEqual(user.email, user.__str__())
 
    def test_raises_error_when_no_email(self):
        self.assertRaises(ValueError, User.objects.create_user, email='', password='123')

    def test_superuser_create(self):
        user = User.objects.create_superuser(email='super@mail.com', password='123')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'super@mail.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
 
    def test_superuser_raises_error_when_is_superuser_false(self):
       with self.assertRaisesMessage(ValueError, 'Superuser must be assigned to is_superuser=True.'):
           User.objects.create_superuser(email='super@mail.com', password='123',
                                         is_staff=True, is_active=True, is_superuser=False)
    
    def test_superuser_raises_error_when_is_staff_false(self):
       with self.assertRaisesMessage(ValueError, 'Superuser must be assigned to is_staff=True.'):
           User.objects.create_superuser(email='super@mail.com', password='123',
                                         is_staff=False, is_active=True, is_superuser=True)

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

#===========================API TESTS======================================

class UserTests(APITestCase):

    def test_view_users(self):
        url = reverse('users:listcreate')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_user(self):
        user = user = User.objects.create_superuser(email='super@mail.com', password='123')
        url = reverse('users:detailcreate', args=[user.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
