from django.test import TestCase

from taxi.forms import (
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


def create_form(license_number):
    return DriverLicenseUpdateForm(data={"license_number": license_number})


class FormsTests(TestCase):
    def test_license_number_is_valid(self):
        self.assertTrue(create_form("QWE12345").is_valid())

    def test_len_licence_number_equal_8(self):
        self.assertFalse(create_form("QWE123456").is_valid())
        self.assertFalse(create_form("QWE1234").is_valid())

    def test_first_3_characters_license_number_uppercase_letters(self):
        self.assertFalse(create_form("qwe12345").is_valid())
        self.assertFalse(create_form("QWe12345").is_valid())

    def test_last_5_characters_license_number_digits(self):
        self.assertFalse(create_form("QWE1234q").is_valid())
        self.assertFalse(create_form("QWEqwert").is_valid())

    def test_driver_search_form(self):
        form_data = {"username": "username"}
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {"model": "model"}
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form_data = {"name": "name"}
        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
