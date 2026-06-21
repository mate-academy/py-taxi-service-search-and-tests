from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm,
)
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="qwerty",
            license_number="ABC12345",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="qwerty",
            license_number="ABC12346",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

    def test_is_valid(self):
        form_data = {
            "model": "M5",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

        car = form.save()
        self.assertEqual(car.model, "M5")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertEqual(car.drivers.count(), len(form_data["drivers"]))

    def test_drivers_field_uses_checkboxes(self):
        form = CarForm()
        self.assertTrue(isinstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        ))


class TestDriverCreationForm(TestCase):
    def test_with_additional_fields(self):
        form_data = {
            "username": "driver1",
            "password1": "fhgkA1754",
            "password2": "fhgkA1754",
            "license_number": "ABC12345",
            "first_name": "Bobby",
            "last_name": "Bob",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

        driver = form.save()
        self.assertEqual(driver.username, "driver1")
        self.assertTrue(driver.check_password("fhgkA1754"))
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertEqual(driver.first_name, "Bobby")
        self.assertEqual(driver.last_name, "Bob")

    def test_with_license_number_length_not_equal_8(self):
        form_data = {
            "username": "driver1",
            "password1": "fhgkA1754",
            "password2": "fhgkA1754",
            "license_number": "ABC123452",
            "first_name": "Bobby",
            "last_name": "Bob",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "ABC123"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_with_license_number_wrong_first_characters(self):
        form_data = {
            "username": "driver1",
            "password1": "fhgkA1754",
            "password2": "fhgkA1754",
            "license_number": "abc12345",
            "first_name": "Bobby",
            "last_name": "Bob",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "12345678"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "$^*45678"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_with_license_number_wrong_last_characters(self):
        form_data = {
            "username": "driver1",
            "password1": "fhgkA1754",
            "password2": "fhgkA1754",
            "license_number": "ABCDEFGH",
            "first_name": "Bobby",
            "last_name": "Bob",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "ABC!@#$%"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestDriverLicenseUpdateForm(TestCase):
    def test_is_valid(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_with_license_number_length_not_equal_8(self):
        form_data = {
            "license_number": "ABC12345678"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "ABC123"
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_with_license_number_wrong_first_characters(self):
        form_data = {
            "license_number": "abc12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "12345678"
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "$^*45678"
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_with_license_number_wrong_last_characters(self):
        form_data = {
            "license_number": "ABCDEFGH",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "ABC!@#$%"
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestDriverUsernameSearchForm(TestCase):
    def test_is_valid(self):
        form_data = {
            "username": "qwerty",
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_label_is_empty_string(self):
        form = DriverUsernameSearchForm()
        self.assertTrue(form.fields["username"].label is None
                        or form.fields["username"].label == "")


class TestCarModelSearchForm(TestCase):
    def test_is_valid(self):
        form_data = {
            "model": "qwerty",
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_label_is_empty_string(self):
        form = CarModelSearchForm()
        self.assertTrue(form.fields["model"].label is None
                        or form.fields["model"].label == "")


class TestManufacturerNameSearchForm(TestCase):
    def test_is_valid(self):
        form_data = {
            "name": "qwerty",
        }
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_label_is_empty_string(self):
        form = ManufacturerNameSearchForm()
        self.assertTrue(form.fields["name"].label is None
                        or form.fields["name"].label == "")
