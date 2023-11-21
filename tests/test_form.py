from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm
from taxi.models import Car, Manufacturer, Driver
from tests.test_view import CAR_URL, DRIVER_URL, MANUFACTURER_URL


class DriverCreationFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "driver1",
            "password1": "test_password123",
            "password2": "test_password123",
            "license_number": "QWE12345",
            "first_name": "Ivan",
            "last_name": "Ivanov"
        }

    def test_create_driver_with_valid_license_number(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_create_driver_with_invalid_license_characters(self):
        self.form_data["license_number"] = "QwE12345"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, self.form_data)

    def test_create_driver_with_invalid_license_digits(self):
        self.form_data["license_number"] = "QWE123G5"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, self.form_data)

    def test_create_driver_with_invalid_license_length(self):
        self.form_data["license_number"] = "QWE1235"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, self.form_data)

    def test_create_driver_with_unmatched_passwords(self):
        self.form_data["password1"] = "test_password129"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, self.form_data)


class SearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="pass12345"
        )
        self.client.force_login(self.user)

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Jeep",
            country="USA"
        )
        first_car = Car.objects.create(
            model="Grand Cherokee",
            manufacturer=manufacturer
        )
        second_car = Car.objects.create(
            model="Gladiator",
            manufacturer=manufacturer
        )
        response = self.client.get(CAR_URL, {"model": first_car})
        self.assertContains(response, first_car)
        self.assertNotContains(response, second_car)

    def test_search_driver_by_username(self):
        driver1 = Driver.objects.create(
            username="ivan",
            password="driver1pass",
            license_number="QWE12345"
        )
        driver2 = Driver.objects.create(
            username="vasiliy",
            password="driver2pass",
            license_number="QWE54321"
        )
        response = self.client.get(DRIVER_URL, {"username": driver1.username})
        self.assertContains(response, driver1.username)
        self.assertNotContains(response, driver2.username)

    def test_search_manufacturer_by_name(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Jeep",
            country="USA"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Dodge",
            country="USA"
        )
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": manufacturer1.name})
        self.assertContains(response, manufacturer1.name)
        self.assertNotContains(response, manufacturer2.name)
