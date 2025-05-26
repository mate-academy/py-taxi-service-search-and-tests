from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm
)


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "license_number": "ABC12345",
            "first_name": "New",
            "last_name": "User",
            "password1": "123user123",
            "password2": "123user123",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form_is_valid(self):
        form = CarSearchForm(data={"model": "Toyota Yaris"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_is_valid(self):
        form = DriverSearchForm(data={"username": "bob.ken"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_is_valid(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())
