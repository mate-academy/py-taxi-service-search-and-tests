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
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test username',
            password='test password',
        )
        self.client.force_login(self.user)
    def test_search_by_manufacturer(self):
        Manufacturer.objects.create(
            name='Tesla',
            country='test country1',
        )
        Manufacturer.objects.create(
            name='BMW',
            country='test country2',
        )
        Manufacturer.objects.create(
            name='Porsche',
            country='test country3',
        )
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": "E"}
        )
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 2)

    def test_search_by_car(self):
        m1 = Manufacturer.objects.create(
            name='test manufacturer1',
            country='test country1',
        )
        m2 = Manufacturer.objects.create(
            name='test manufacturer2',
            country='test country2',
        )
        m3 = Manufacturer.objects.create(
            name='test manufacturer3',
            country='test country3',
        )

        Car.objects.create(
            model='AMG',
            manufacturer=m1,
        )
        Car.objects.create(
            model='X5',
            manufacturer=m2,
        )
        Car.objects.create(
            model='Huracan',
            manufacturer=m3,
        )
        response = self.client.get(
            CAR_LIST_URL,
            {"model": "a"}
        )
        cars = response.context["car_list"]
        self.assertEqual(len(cars), 2)

    def test_search_by_driver(self):
        get_user_model().objects.create_user(
            username='Mike',
            password='test password1',
            license_number='DDD23232',
        )
        get_user_model().objects.create_user(
            username='Jess',
            password='test password2',
            license_number='VDD23232',
        )
        get_user_model().objects.create_user(
            username='Kenny',
            password='test password3',
            license_number='DAD23232',
        )
        response = self.client.get(
            DRIVER_LIST_URL,
            {"username": "nn"}
        )
        drivers = response.context["driver_list"]
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, 'Kenny')
