from django.test import TestCase
from django.forms.widgets import TextInput, CheckboxSelectMultiple

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class DriverFormsTests(TestCase):
    def test_driver_creation_form_with_driver_license_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12345test",
            "password2": "user12345test",
            "license_number": "TET00000",
            "first_name": "test first",
            "last_name": "test last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_with_driver_license_is_valid(self):
        form_data = {
            "license_number": "TET00000",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form_username_has_correct_widget(self):
        form = DriverSearchForm
        self.assertTrue("username" in form.base_fields)
        self.assertIsInstance(form.base_fields["username"].widget, TextInput)
        self.assertTrue(
            "placeholder" in form.base_fields["username"].widget.attrs
        )

    def test_car_form_drivers_has_correct_widget(self):
        form = CarForm
        self.assertTrue("drivers" in form.base_fields)
        self.assertIsInstance(
            form.base_fields["drivers"].widget,
            CheckboxSelectMultiple
        )

    def test_car_search_form_model_has_correct_widget(self):
        form = CarSearchForm
        self.assertTrue("model" in form.base_fields)
        self.assertIsInstance(form.base_fields["model"].widget, TextInput)
        self.assertTrue(
            "placeholder" in form.base_fields["model"].widget.attrs
        )

    def test_manufacturer_search_form_name_has_correct_widget(self):
        form = ManufacturerSearchForm
        self.assertTrue("name" in form.base_fields)
        self.assertIsInstance(form.base_fields["name"].widget, TextInput)
        self.assertTrue(
            "placeholder" in form.base_fields["name"].widget.attrs
        )


class DriverLicenseValidationForms(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_validation_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("TES12345").is_valid())

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertFalse(self.create_form("TES123456").is_valid())

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertFalse(self.create_form("TES1234").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("TE123456").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("TEST2345").is_valid())
