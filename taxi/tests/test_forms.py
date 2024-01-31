from django.forms import CheckboxSelectMultiple
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import Driver
from taxi.views import DriverListView


class DriverFormsTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "test_password12",
            "password2": "test_password12",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "license_number": "VDG12345",
        }
        self.update_form_data = {"license_number": "VDG12345"}
        self.incorrect_digits_and_length_update_form_data = {
            "license_number": "VDG1245"
        }
        self.incorrect_upper_first_three_letter_form_data = {
            "license_number": "Vdg12345"
        }
        self.incorrect_length_form_data = {"license_number": "VDH123456"}

    def test_driver_creation_with_cleaned_license_number_form(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_update_driver_license_number_form(self):
        correct_form = DriverLicenseUpdateForm(data=self.update_form_data)

        incorrect_digit_form = DriverLicenseUpdateForm(
            data=self.incorrect_digits_and_length_update_form_data
        )

        incorrect_upper_first_three_letter_form = DriverLicenseUpdateForm(
            data=self.incorrect_upper_first_three_letter_form_data
        )

        self.assertTrue(correct_form.is_valid())
        self.assertFalse(incorrect_digit_form.is_valid())
        self.assertFalse(incorrect_upper_first_three_letter_form.is_valid())


class CarTestsTest(TestCase):

    def test_car_checkbox_form(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget, CheckboxSelectMultiple
        )


class SearchFormsTest(TestCase):
    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "user1"})
        self.assertTrue(form.is_valid())

        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

        form = DriverSearchForm(data={"username": "a" * 101})
        self.assertFalse(form.is_valid())

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Car 1"})
        self.assertTrue(form.is_valid())

        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

        form = CarSearchForm(data={"model": "a" * 256})
        self.assertFalse(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Manufacturer 1"})
        self.assertTrue(form.is_valid())

        form = ManufacturerSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

        form = ManufacturerSearchForm(data={"name": "a" * 256})
        self.assertFalse(form.is_valid())
