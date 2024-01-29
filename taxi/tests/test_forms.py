from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse('taxi:driver-list')


class DriverListViewTest(TestCase):
    def setUp(self):
        # Create a test user
        user = get_user_model()
        self.user = user.objects.create(username='test_user', password='test_password')

        # Create some test drivers with unique license numbers
        self.driver1 = Driver.objects.create(username='driver1', license_number='license1')
        self.driver2 = Driver.objects.create(username='driver2', license_number='license2')
        self.driver3 = Driver.objects.create(username='driver3', license_number='license3')

    def test_search_view_with_results(self):
        # Login the test user
        self.client.login(username='test_user', password='test_password')

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
        self.client.login(username='test_user', password='test_password')

        # Make a GET request with a search query
        response = self.client.get(DRIVER_LIST_URL, {'username': 'non_existent_driver'})

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the search form is in the context
        self.assertIn('search_form', response.context)

        # Check that the search form has the correct initial value
        self.assertEqual(response.context['search_form'].initial['username'], 'non_existent_driver')

        # Check that there are no matching drivers in the object list
        self.assertNotContains(response, 'driver1')
        self.assertNotContains(response, 'driver2')
        self.assertNotContains(response, 'driver3')
#
