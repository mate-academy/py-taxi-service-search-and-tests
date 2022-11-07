from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_CREATE = reverse("taxi:driver-create")


class PublicManufacturerList(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerList(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("Test", "Pass11243fd")
        self.client.force_login(self.user)

    def test_pagination_is_five(self):
        number_of_manufacturers = 10
        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Toyota {manufacturer_id}",
                country=f"Japan {manufacturer_id}",
            )

        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturer)
        )

    def test_correct_template_used(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarList(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarList(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testName",
            password="tEst12345_",
            license_number="RTX30901",
        )
        self.client.force_login(self.user)

    def test_car_list_private(self):
        manufacturer = Manufacturer.objects.create(
            name="Testtt", country="TEstA"
        )
        Car.objects.create(model="testModel", manufacturer=manufacturer)

        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))

    def test_correct_template_used(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_CREATE)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "Test", "TestPass1231234"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "test_pass123",
            "password2": "test_pass123",
            "first_name": "Test first_name",
            "last_name": "Test last_name",
            "license_number": "TST12243",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
