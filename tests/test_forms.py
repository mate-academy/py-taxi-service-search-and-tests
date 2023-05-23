from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarModelSearchForm,
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm,
)
from taxi.models import Car, Manufacturer


class DriverCreateAndUpdateFormsTests(TestCase):
    def test_driver_create_form_with_data_is_valid(self) -> None:
        driver_data = {
            "username": "UserOne",
            "first_name": "One",
            "last_name": "Two",
            "password1": "Tree12344",
            "password2": "Tree12344",
            "license_number": "ETH17511",
        }

        form = DriverCreationForm(data=driver_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, driver_data)

    def test_driver_update_license_nums_form_is_valid(self) -> None:
        driver_new_plates = {
            "license_number": "SOL19535",
        }

        form = DriverLicenseUpdateForm(data=driver_new_plates)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, driver_new_plates)


class SearchFormsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Admin123",
            password="TestPas2345"
        )
        self.client.force_login(self.user)

        self.manufacturer_one = Manufacturer.objects.create(
            name="Lexus",
            country="Japan",
        )
        self.manufacturer_two = Manufacturer.objects.create(
            name="Peugeot",
            country="France",
        )

    def test_car_search_form_get_correct_result(self) -> None:
        self.car1 = Car.objects.create(
            model="Lexus NX",
            manufacturer=self.manufacturer_one,
        )
        self.car2 = Car.objects.create(
            model="Peugeot 308SW",
            manufacturer=self.manufacturer_two,
        )

        url = "/cars/"
        car_search_data = {"model": "Lexus"}

        response = self.client.get(url, data=car_search_data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            CarModelSearchForm,
        )
        self.assertEqual(
            response.context["search_form"].initial["model"],
            "Lexus",
        )

    def test_driver_search_form_get_correct_result(self) -> None:
        self.driver_one = get_user_model().objects.create_user(
            username="Admin_one",
            password="Qwert123",
            license_number="QWE12345",
        )
        self.driver_two = get_user_model().objects.create_user(
            username="Second",
            password="super.driver",
            license_number="QWE33454",
        )

        url = "/drivers/"
        driver_search_data = {"username": "admin"}

        response = self.client.get(url, data=driver_search_data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            DriverUsernameSearchForm,
        )
        self.assertEqual(
            response.context["search_form"].initial["username"],
            "admin",
        )

    def test_manufacturer_search_form_get_correct_result(self) -> None:
        url = "/manufacturers/"
        manufacturer_search_data = {"name": "Lexus"}

        response = self.client.get(url, data=manufacturer_search_data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            ManufacturerNameSearchForm,
        )
        self.assertEqual(
            response.context["search_form"].initial["name"],
            "Lexus",
        )
