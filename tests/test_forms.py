from django.test import TestCase

from taxi.models import Manufacturer
from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm,
                        ManufacturerNameSearchForm,
                        CarModelSearchForm,
                        DriverUsernameSearchForm)


class FieldsFormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test_username",
            "password1": "TestPassword",
            "password2": "TestPassword",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "license_number": "ABC12345"
        }

    def test_fields_for_driver_creation_form(self):
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")
        self.assertEqual(form.cleaned_data["first_name"], "TestFirstName")
        self.assertEqual(form.cleaned_data["last_name"], "TestLastName")

    def test_fields_for_driver_license_update_form(self):
        form = DriverLicenseUpdateForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertNotEqual(form.cleaned_data, self.form_data)
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")
        self.assertEqual(form.cleaned_data.get("first_name", " "), " ")
        self.assertEqual(form.cleaned_data.get("last_name", " "), " ")


class CleanLicenseNumberTest(TestCase):
    def test_update_license_number_with_non_valid_date(self):
        form_date = {"license_number": "abc1235"}
        form = DriverLicenseUpdateForm(form_date)
        self.assertFalse(form.is_valid())


class SearchFormTest(TestCase):
    def setUp(self) -> None:
        for manufacturer_id in range(3):
            Manufacturer.objects.create(
                name=f"Test Name-{manufacturer_id}",
                country=f"Test Country-{manufacturer_id}")

    def test_manufacturer_search_form(self):
        form_data = {"name": "test"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {"model": "test"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form_data = {"username": "test"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
