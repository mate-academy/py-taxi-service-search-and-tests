from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer

CarsListView = reverse("taxi:car-list")
DriversListView = reverse("taxi:driver-list")
ManufacturersListView = reverse("taxi:manufacturer-list")


class PublicTaxiTests(TestCase):

    def test_login_required(self):
        response = self.client.get(CarsListView)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaxiSearchAndFeatureTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        # Створюємо тестові дані для перевірки пошуку
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer2
        )

        self.driver2 = Driver.objects.create_user(
            username="speedy_driver",
            password="password123",
            license_number="XYZ98765"
        )

    def test_car_search_by_model(self):
        response = self.client.get(CarsListView, {"model": "corolla"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)

    def test_car_search_empty(self):
        response = self.client.get(CarsListView, {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)

    def test_driver_search_by_username(self):
        response = self.client.get(DriversListView, {"username": "speedy"})
        self.assertEqual(response.status_code, 200)

        self.assertIn(self.driver2, response.context["driver_list"])
        self.assertNotIn(self.user, response.context["driver_list"])

    def test_manufacturer_search_by_name(self):
        response = self.client.get(ManufacturersListView, {"name": "toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
