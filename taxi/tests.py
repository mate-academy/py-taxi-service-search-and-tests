from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q

from taxi.models import Manufacturer, Car, Driver

User = get_user_model()


class SearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test manufacturers
        self.manufacturer1 = Manufacturer.objects.create(
            name='Toyota',
            country='Japan'
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name='Ford',
            country='USA'
        )

        # Create test cars
        self.car1 = Car.objects.create(
            model='Corolla',
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model='Focus',
            manufacturer=self.manufacturer2
        )

        # Create test drivers
        self.driver1 = User.objects.create_user(
            username='john_doe',
            first_name='John',
            last_name='Doe',
            license_number='LIC123',
            password='testpass123'
        )
        self.driver2 = User.objects.create_user(
            username='jane_smith',
            first_name='Jane',
            last_name='Smith',
            license_number='LIC456',
            password='testpass123'
        )

        # Login a test user
        self.client.login(username='john_doe', password='testpass123')


class ManufacturerSearchTests(SearchTestCase):
    def test_manufacturer_search_by_name(self):
        response = self.client.get(reverse('taxi:manufacturer-list'), {'q': 'Toyota'})
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)

    def test_manufacturer_partial_search(self):
        response = self.client.get(reverse('taxi:manufacturer-list'), {'q': 'ord'})
        self.assertContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer1.name)


class CarSearchTests(SearchTestCase):
    def test_car_search_by_model(self):
        response = self.client.get(reverse('taxi:car-list'), {'q': 'Corolla'})
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)


class DriverSearchTests(SearchTestCase):
    def test_driver_search_by_license(self):
        response = self.client.get(reverse('taxi:driver-list'), {'q': 'LIC456'})
        self.assertContains(response, self.driver2.username)


class PaginationWithSearchTests(SearchTestCase):
    def test_pagination_maintains_search(self):
        # First ensure we have enough manufacturers to trigger pagination
        for i in range(10):
            Manufacturer.objects.create(
                name=f"Test Manufacturer {i}",
                country="Test Country"
            )

        response = self.client.get(reverse('taxi:manufacturer-list'), {
            'q': 'Test',
            'page': '1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'q=Test')
