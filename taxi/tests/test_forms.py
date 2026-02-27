from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm
from taxi.models import Manufacturer


class DriverLicenseUpdateFormTest(TestCase):
    def test_check_is_valid_in_form_update(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})

        self.assertTrue(form.is_valid())

    def test_check_no_valid_letters_in_form_update(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"][0], "First 3 characters should be uppercase letters")

    def test_check_no_valid_length_in_form_update(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345678"})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"][0], "License number should consist of 8 characters")

    def test_check_no_valid_5_last_numbers_in_form_update(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12ao5"})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"][0], "Last 5 characters should be digits")

class DriverCreationFormTest(TestCase):
    def test_check_custom_fields_in_driver_creation_form(self):
        form = DriverCreationForm()

        self.assertIn("license_number", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)

class CarFormTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="John",
            last_name="Wick",
            email="john_wick@.lol"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_is_valid_car_form(self):
        form = CarForm(data={"model":"X6", "manufacturer": self.manufacturer.pk, "drivers": [self.driver.pk]})

        self.assertTrue(form.is_valid())

    def test_no_valid_car_form(self):
        form = CarForm(data={"model":"X6", "drivers": [self.driver.pk]})

        self.assertFalse(form.is_valid())