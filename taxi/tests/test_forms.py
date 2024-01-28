from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse('taxi:driver-list')


class DriverListViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some test drivers
        self.driver1 = Driver.objects.create(username='driver1')
        self.driver2 = Driver.objects.create(username='driver2')
        self.driver3 = Driver.objects.create(username='driver3')

    def test_search_view_with_results(self):
        # Login the test user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request with a search query
        response = self.client.get(DRIVER_LIST_URL, {'username': 'driver2'})

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the search form is in the context
        self.assertIn('search_form', response.context)

        # Check that the search form has the correct initial value
        self.assertEqual(response.context['search_form'].initial['username'], 'driver2')

        # Check that only the matching driver is in the object list
        self.assertContains(response, 'driver2')
        self.assertNotContains(response, 'driver1')
        self.assertNotContains(response, 'driver3')

    def test_search_view_with_no_results(self):
        # Login the test user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request with a search query
        response = self.client.get(DRIVER_LIST_URL, {'username': 'nonexistentdriver'})

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the search form is in the context
        self.assertIn('search_form', response.context)

        # Check that the search form has the correct initial value
        self.assertEqual(response.context['search_form'].initial['username'], 'nonexistentdriver')

        # Check that there are no matching drivers in the object list
        self.assertNotContains(response, 'driver1')
        self.assertNotContains(response, 'driver2')
        self.assertNotContains(response, 'driver3')
#
