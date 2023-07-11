from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, ManufacturerSearchForm, CarSearchForm


class FormTest(TestCase):
    @staticmethod
    def create_form(license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": license_number}
        )

    def test_license_number_is_valid(self):
        self.assertTrue(self.create_form("ABC12345").is_valid())

    def test_license_number_len_not_equals_8(self):
        self.assertFalse(self.create_form("ABCDEFG12345").is_valid())
        self.assertFalse(self.create_form("ABC123").is_valid())

    def test_license_number_first_3_must_be_letters(self):
        self.assertFalse(self.create_form("ABCD12345").is_valid())

    def test_license_number_last_5_must_be_numbers(self):
        self.assertFalse(self.create_form("ABC123451231312").is_valid())

    def test_manufacturer_search_form(self):
        form_data = {"name": "test"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form_data = {"model": "Mazda"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
