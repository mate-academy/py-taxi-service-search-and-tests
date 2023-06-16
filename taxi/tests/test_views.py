from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicListTest(TestCase):
    def test_login_required(self):
        manufacturer_list_res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEquals(manufacturer_list_res.status_code, 200)

        car_list_res = self.client.get(CAR_LIST_URL)
        self.assertNotEquals(car_list_res.status_code, 200)

        driver_list_res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEquals(driver_list_res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tests",
            password="test1234",
            license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Volvo", country="Sweden")
        Manufacturer.objects.create(name="Honda", country="Japan")

        response = self.client.get(MANUFACTURER_LIST_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testCAR",
            password="test1234",
            license_number="CAR12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        user = get_user_model().objects.create_user(
            username="tests",
            password="test1234",
            license_number="TES12345"
        )
        volvo = Manufacturer.objects.create(name="Volvo", country="Sweden")
        self.car = Car.objects.create(id=1, model="V50", manufacturer=volvo)
        self.car.drivers.add(user)
        self.car.save()
        response_list = self.client.get(CAR_LIST_URL)
        cars = Car.objects.select_related("manufacturer")

        self.assertEquals(response_list.status_code, 200)
        self.assertEquals(
            list(response_list.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response_list, "taxi/car_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tests",
            password="test1234",
            license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):

        drivers = Driver.objects.all()
        response_list = self.client.get(DRIVER_LIST_URL)
        self.assertEquals(response_list.status_code, 200)
        self.assertEquals(
            list(response_list.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response_list, "taxi/driver_list.html")

    def test_pagination_is_five(self):
        for driver_id in range(9):
            get_user_model().objects.create_user(
                username=f"tests{driver_id}",
                password="test1234",
                license_number=f"DES1234{driver_id}"
            )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)
