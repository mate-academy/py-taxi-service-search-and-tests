from django.forms import CharField
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", args=[1])
DRIVER_CREATE_URL = reverse("taxi:driver-create")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class TestSearchForms(TestCase):
    @classmethod
    def setUpTestData(cls):
        objects_number = 4

        for number in range(0, objects_number):
            Manufacturer.objects.create(
                name=f"test_name{number}",
                country=f"test_country{number}"
            )

            Driver.objects.create_user(
                username=f"testuser{number}",
                password=f"test1234user{number}",
                license_number=f"12{number}ASDFG"
            )

            Car.objects.create(
                model=f"model{number}",
                manufacturer=Manufacturer.objects.get(id=number + 1)
            )

    def test_search_form_on_site_pages_exist(self):
        test_cases = [
            (
                "test_car_search_form",
                CAR_LIST_URL,
                "car_search_form"
            ),
            (
                "test_driver_search_form",
                DRIVER_LIST_URL,
                "driver_search_form"
            ),
            (
                "test_manufacturer_search_form",
                MANUFACTURER_LIST_URL,
                "manufacturer_search_form"
            )
        ]

        self.client.force_login(
            Driver.objects.get(id=1)
        )

        for test_name, url, context_name in test_cases:
            with self.subTest(test_name):
                response = self.client.get(url)

                self.assertTrue(context_name in response.context)


class TestLicenseNumberValidation(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="username1",
            password="user1234name"
        )

    def test_license_number_create_form_validation(self):
        self.client.force_login(
            Driver.objects.get(id=1)
        )

        test_cases = [
            (
                "test_driver_create_license_validation_with_two_letters",
                DRIVER_CREATE_URL,
                {"license_number": "AS123456"},
                "First 3 characters should be uppercase letters"
            ),
            (
                "test_driver_create_license_validation_with_nine_characters",
                DRIVER_CREATE_URL,
                {"license_number": "ASD123456"},
                "License number should consist of 8 characters"
            ),
            (
                "test_driver_create_license_validation_with_four_letter",
                DRIVER_CREATE_URL,
                {"license_number": "ABSD2346"},
                "Last 5 characters should be digits"
            )
        ]

        for test_name, url, data, error_text in test_cases:
            with self.subTest(test_name):
                response = self.client.post(url, data)
                self.assertContains(response, error_text, html=True)

    def test_license_number_update_form_validation(self):
        self.client.force_login(
            Driver.objects.get(id=1)
        )

        test_cases = [
            (
                "test_driver_update_license_validation_with_two_letters",
                DRIVER_UPDATE_URL,
                {"license_number": "AS123456"},
                "First 3 characters should be uppercase letters"
            ),
            (
                "test_driver_update_license_validation_with_nine_characters",
                DRIVER_UPDATE_URL,
                {"license_number": "ASD123456"},
                "License number should consist of 8 characters"
            ),
            (
                "test_driver_update_license_validation_with_four_letter",
                DRIVER_UPDATE_URL,
                {"license_number": "ABSD2346"},
                "Last 5 characters should be digits"
            )
        ]

        for test_name, url, data, error_text in test_cases:
            with self.subTest(test_name):
                response = self.client.post(url, data)
                self.assertContains(response, error_text, html=True)
