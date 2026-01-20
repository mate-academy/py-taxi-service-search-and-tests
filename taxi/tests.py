from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Driver

class DriverSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        user1 = User.objects.create_user(username='driver1', password='testpass123')
        user2 = User.objects.create_user(username='driver2', password='testpass123')
        self.driver1 = Driver.objects.create(user=user1)
        self.driver2 = Driver.objects.create(user=user2)

    def test_search_by_username(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('driver_list'), {'q': 'driver1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'driver1')
        self.assertNotContains(response, 'driver2')

    def test_no_search_query(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('driver_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'driver1')
        self.assertContains(response, 'driver2')
