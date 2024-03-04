from django.contrib.auth import get_user_model

from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

MANUFACTURER_URL = "taxi:manufacturer-list"
CAR_URL = "taxi:car-list"
DRIVER_URL = "taxi:driver-list"


class PublicViewTest(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateViewTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        self.driver = Driver.objects.create(
            username="test_driver",
            password="<PASSWORD>",
            license_number="test_license_number"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )

        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<PASSWORD>"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        response = self.client.get(reverse(MANUFACTURER_URL))
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_driver(self):
        response = self.client.get(reverse(DRIVER_URL))
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_car(self):
        response = self.client.get(reverse(CAR_URL))
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_should_filter_manufacturer_list(self):
        response = self.client.get(reverse(MANUFACTURER_URL))
        self.assertEqual(
            response.context_data["manufacturer_list"][0],
            self.manufacturer
        )

    def test_search_should_filter_driver_list(self):
        response = self.client.get(reverse(DRIVER_URL))
        self.assertEqual(response.context_data["driver_list"][0], self.driver)

    def test_search_should_filter_car_list(self):
        response = self.client.get(reverse(CAR_URL))
        self.assertEqual(response.context_data["car_list"][0], self.car)
