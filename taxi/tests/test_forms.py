from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormsTest(TestCase):
    def test_driver_creation_form_with_first_and_last_names_and_license(self):
        form_data = {
            "username": "rambo1982",
            "password1": "JustWantToEatButHaveToKill82",
            "password2": "JustWantToEatButHaveToKill82",
            "first_name": "John",
            "last_name": "Rambo",
            "license_number": "RAM19821"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_driver_creation_form_with_invalid_username(self):
        form_data = {
            "username": "",
            "password1": "JustWantToEatButHaveToKill82",
            "password2": "JustWantToEatButHaveToKill82",
            "first_name": "John",
            "last_name": "Rambo",
            "license_number": "RAM19821"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_form_valid(self):
        form_data = {"license_number": "RAM19821"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form_data = {"license_number": "terminator"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_search_form_valid(self):
        form_data = {"model": "M3"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_invalid(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_valid(self):
        form_data = {"username": "rambo1982"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_invalid(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form_data = {"name": "BMW"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_invalid(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestValidateLicenseNumber(TestCase):

    def test_valid_license_number(self):
        valid_license_number = "TST12345"
        result = validate_license_number(valid_license_number)
        self.assertEqual(result, valid_license_number)

    def test_invalid_length(self):
        invalid_license_number = "TEST"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_first_three_characters(self):
        invalid_license_number = "12345678"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_last_five_characters(self):
        invalid_license_number = "TES1234T"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_case(self):
        invalid_license_number = "tst12345"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)
