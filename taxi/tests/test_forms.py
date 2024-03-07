from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, SearchForm
from taxi.models import Manufacturer, Car
from taxi.tests.test_config import (
    DRIVER_LIST_URL,
    CAR_LIST_URL,
    MANUFACTURER_LIST_URL
)


class DriverFormsTests(TestCase):

    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="Password123!"
        )
        self.client.force_login(self.driver)

    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "new-driver",
            "password1": "Driver12test!",
            "password2": "Driver12test!",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "TST47831"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_create_driver(self):
        form_data = {
            "username": "new-driver",
            "password1": "Driver12test!",
            "password2": "Driver12test!",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "TST47831"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )


class LicenseNumberValidationTests(TestCase):
    @staticmethod
    def update_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_license_number_is_valid(self):
        self.assertTrue(self.update_form("TST12345").is_valid())

    def test_license_number_min_length_is_8(self):
        self.assertFalse(self.update_form("TST1234").is_valid())

    def test_license_number_max_length_is_8(self):
        self.assertFalse(self.update_form("TST123456").is_valid())

    def test_3_first_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.update_form("TsT12345").is_valid())

    def test_5_last_characters_should_be_numbers(self):
        self.assertFalse(self.update_form("TST1245s").is_valid())


class SearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="Driver1test!",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Bugatti",
            country="Italy"
        )
        self.car = Car.objects.create(
            model="Veyron",
            manufacturer=self.manufacturer
        )

    def test_driver_username_search_form(self):
        form_data = {"username": self.user.username}

        form = SearchForm(search_field="username", data=form_data)
        response = self.client.get(DRIVER_LIST_URL, data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_car_model_search_form(self):
        form_data = {"model": self.car.model}

        form = SearchForm(search_field="model", data=form_data)
        response = self.client.get(CAR_LIST_URL, data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

    def test_car_model_search_no_results(self):
        form_data = {"model": "Tesla"}

        response = self.client.get(CAR_LIST_URL, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.car.model)

    def test_manufacturer_name_search_form(self):
        form_data = {"name": self.manufacturer.name}

        form = SearchForm(search_field="name", data=form_data)
        response = self.client.get(MANUFACTURER_LIST_URL, data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)

    def test_manufacturer_name_search_no_results(self):
        form_data = {"name": "Tesla"}

        response = self.client.get(MANUFACTURER_LIST_URL, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.car.model)
