from django.test import SimpleTestCase

from taxi.forms import (DriverSearchForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        DriverLicenseUpdateForm)


class FormsTest(SimpleTestCase):
    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "Test username"})
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "Test model"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Test name"})
        self.assertTrue(form.is_valid())


class DriverLicenseUpdateFormTest(SimpleTestCase):
    def setUp(self):
        self.form_data = {"username": "test",
                          "password1": "passwordstrong",
                          "password2": "passwordstrong",
                          "license_number": "AAA123456"}

    def test_short_number(self):
        self.form_data["license_number"] = "DDR1111"
        form = DriverLicenseUpdateForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_too_long_number(self):
        self.form_data["license_number"] += "1"
        form = DriverLicenseUpdateForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_first_three_number_not_is_upper_case(self):
        self.form_data["license_number"] = "aaa123456"
        form = DriverLicenseUpdateForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_last_numbers_is_not_digits(self):
        self.form_data["license_number"] = "aaabbbbb"
        form = DriverLicenseUpdateForm(data=self.form_data)
        self.assertFalse(form.is_valid())
