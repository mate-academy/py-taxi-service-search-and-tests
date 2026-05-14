from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        CarSearchForm,
                        DriverSearchForm,
                        ManufacturerSearchForm)


class FormsTests(TestCase):
    def test_driver_creation_form_with_license(self):
        form_data = {
            "username": "firstuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "ABC12345",
            "first_name": "test",
            "last_name": "test",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")
        self.assertEqual(form.cleaned_data["username"], "firstuser")

    def test_car_search_form_is_valid(self):
        form_data = {
            "model": "test",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_is_valid(self):
        form_data = {
            "username": "test",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_is_valid(self):
        form_data = {
            "name": "test",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
