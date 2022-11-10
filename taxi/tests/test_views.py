from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", args=[1])
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", args=[1])
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", args=[1])
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", args=[1])
CAR_DELETE_URL = reverse("taxi:car-delete", args=[1])
CAR_ASSIGN_URL = reverse("taxi:toggle-car-assign", args=[1])

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", args=[1])
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", args=[1])
DRIVER_DELETE_URL = reverse("taxi:driver-delete", args=[1])


class PublicManufacturerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_manufacturer_login_required(self):
        test_cases = [
            (
                "test_manufacturer_list_login_required",
                MANUFACTURER_LIST_URL,
                200
            ),
            (
                "test_manufacturer_delete_login_required",
                MANUFACTURER_DELETE_URL,
                200
            ),
            (
                "test_manufacturer_update_login_required",
                MANUFACTURER_UPDATE_URL,
                200
            ),
            (
                "test_manufacturer_create_login_required",
                MANUFACTURER_CREATE_URL,
                200
            )
        ]

        for test_name, url, result in test_cases:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, result)


class PublicCarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        driver = Driver.objects.create_user(
            username="username1",
            password="user1234name"
        )
        car = Car.objects.create(model="M3", manufacturer=manufacturer)
        car.drivers.add(driver)

    def test_car_login_required(self):
        test_cases = [
            (
                "test_car_list_login_required",
                CAR_LIST_URL,
                200
            ),
            (
                "test_car_detail_login_required",
                CAR_DETAIL_URL,
                200
            ),
            (
                "test_car_create_login_required",
                CAR_CREATE_URL,
                200
            ),
            (
                "test_car_update_login_required",
                CAR_UPDATE_URL,
                200
            ),
            (
                "test_car_delete_login_required",
                CAR_DELETE_URL,
                200
            ),
            (
                "test_car_assign_loginrequired",
                CAR_ASSIGN_URL,
                200
            )
        ]

        for test_name, url, result in test_cases:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertNotEqual(response.status_code, result)


class PublicDriverTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="test_user",
            password="test12345USER",
        )

    def test_driver_login_required(self):
        test_cases = [
            (
                "test_driver_list_login_required",
                DRIVER_LIST_URL,
                200
            ),
            (
                "test_driver_detail_login_required",
                DRIVER_DETAIL_URL,
                200
            ),
            (
                "test_driver_create_login_required",
                DRIVER_CREATE_URL,
                200
            ),
            (
                "test_driver_update_login_required",
                DRIVER_UPDATE_URL,
                200
            ),
            (
                "test_driver_delete_login_required",
                DRIVER_DELETE_URL,
                200
            )
        ]

        for test_name, url, result in test_cases:
            response = self.client.get(url)
            with self.subTest(test_name):
                self.assertNotEqual(response.status_code, 200)


class TestPagination(TestCase):
    @classmethod
    def setUpTestData(cls):
        objects_number = 7

        for number in range(0, objects_number):
            Manufacturer.objects.create(
                name=f"test_name{number}",
                country=f"test_country{number}"
            )

            Driver.objects.create_user(
                username=f"testuser{number}",
                password=f"test1234user{number}",
                license_number=f"ABC1234{number}"
            )

            Car.objects.create(
                model=f"model{number}",
                manufacturer=Manufacturer.objects.get(id=number + 1)
            )

    def test_pagination(self):
        self.client.force_login(
            Driver.objects.get(id=1)
        )

        test_cases = [
            (
                "test_manufacturer_list_pagination",
                MANUFACTURER_LIST_URL,
                "manufacturer_list"
            ),
            (
                "test_driver_list_pagination",
                DRIVER_LIST_URL,
                "driver_list"
            ),
            (
                "test_car_list_pagination",
                CAR_LIST_URL,
                "car_list"
            )
        ]
        for test_name, url, context_name in test_cases:
            with self.subTest(test_name):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                self.assertTrue("is_paginated" in response.context)
                self.assertEqual(len(response.context[context_name]), 5)


class PrivateManufacturerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Driver.objects.create_user(
            username="test_user",
            password="test12345USER",
        )

    def test_private_retrive_manufacturer(self):
        test_cases = [
            (
                "test_public_manufacturer_list",
                MANUFACTURER_LIST_URL,
                200
            ),
            (
                "test_public_manufacturer_delete",
                MANUFACTURER_DELETE_URL,
                200
            ),
            (
                "test_public_manufacturer_update",
                MANUFACTURER_UPDATE_URL,
                200
            ),
            (
                "test_public_manufacturer_create",
                MANUFACTURER_CREATE_URL,
                200
            )
        ]

        self.client.force_login(
            Driver.objects.get(id=1)
        )

        for test_name, url, result in test_cases:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, result)


class PrivateCarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        driver = Driver.objects.create_user(
            username="username1",
            password="user1234name"
        )
        car = Car.objects.create(model="M3", manufacturer=manufacturer)
        car.drivers.add(driver)

    def test_private_retrive_car(self):
        test_cases = [
            (
                "test_private_car_list",
                CAR_LIST_URL,
                200
            ),
            (
                "test_private_car_detail",
                CAR_DETAIL_URL,
                200
            ),
            (
                "test_private_car_create",
                CAR_CREATE_URL,
                200
            ),
            (
                "test_private_car_update",
                CAR_UPDATE_URL,
                200
            ),
            (
                "test_private_car_delete",
                CAR_DELETE_URL,
                200
            ),
            (
                "test_private_car_assign",
                CAR_ASSIGN_URL,
                302
            )
        ]

        self.client.force_login(
            Driver.objects.get(id=1)
        )

        for test_name, url, result in test_cases:
            with self.subTest(test_name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, result)


class PrivateDriverTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="test_user",
            password="test12345USER",
        )

    def test_private_retrive_driver(self):
        test_cases = [
            (
                "test_private_driver_list",
                DRIVER_LIST_URL,
                200
            ),
            (
                "test_private_driver_detail",
                DRIVER_DETAIL_URL,
                200
            ),
            (
                "test_private_driver_create",
                DRIVER_CREATE_URL,
                200
            ),
            (
                "test_private_driver_update",
                DRIVER_UPDATE_URL,
                200
            ),
            (
                "test_private_driver_delete",
                DRIVER_DELETE_URL,
                200
            )
        ]

        self.client.force_login(
            Driver.objects.get(id=1)
        )

        for test_name, url, result in test_cases:
            response = self.client.get(url)
            with self.subTest(test_name):
                self.assertEqual(response.status_code, 200)
