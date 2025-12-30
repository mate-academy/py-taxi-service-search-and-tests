from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicViewTests(TestCase):
    def test_login_required_for_manufacturers(self):
        manufacturer_list_response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(manufacturer_list_response.status_code, 200)

    def test_login_required_for_cars(self):
        car_list_response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(car_list_response.status_code, 200)

    def test_login_required_for_drivers(self):
        driver_list_response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(driver_list_response.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test username',
            password='test password',
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        all_manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(all_manufacturers)
        )

    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        all_cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(all_cars)
        )

    def test_retrieve_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        all_drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(all_drivers)
        )


class SearchViewTests(TestCase):
    def test_search_by_manufacturer(self):
        name = {
            "name": "test manufacturer",
        }
        form = ManufacturerSearchForm(data=name)
        self.assertTrue(form.is_valid())

    def test_search_by_car(self):
        model = {
            "model": "test car",
        }
        form = CarSearchForm(data=model)
        self.assertTrue(form.is_valid())

    def test_search_by_driver(self):
        username = {
            "username": "test username",
        }
        form = DriverSearchForm(data=username)
        self.assertTrue(form.is_valid())
