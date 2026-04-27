from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class DriverFormValidationTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12pass",
            "password2": "user12pass",
            "first_name": "Test frist name",
            "last_name": "Test last name",
            "license_number": "AFS12441"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

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


class DriverSearchFormTests(TestCase):
    def test_driver_search_form_empty_input_is_valid(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_valid_input(self):
        form = DriverSearchForm(data={"username": "admin"})
        self.assertTrue(form.is_valid())


class CarSearchFormTests(TestCase):
    def test_car_search_form_empty_input_is_valid(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid_input(self):
        form = CarSearchForm(data={"model": "Mitsubishi Lancer"})
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTests(TestCase):
    def test_manufacturer_search_form_empty_input_is_valid(self):
        form = ManufacturerSearchForm(
            data={"name": ""}
        )
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid_input(self):
        form = ManufacturerSearchForm(
            data={"name": "BMW"}
        )
        self.assertTrue(form.is_valid())
