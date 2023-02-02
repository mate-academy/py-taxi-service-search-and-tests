from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class DriverFormTests(TestCase):
    def test_driver_creation_form_with_additional_fields_are_valid(self):
        driver_data = {
            "username": "New_User",
            "password1": "Test_Password",
            "password2": "Test_Password",
            "first_name": "Firstname",
            "last_name": "Lastname",
            "license_number": "XXX12345",
        }
        form = DriverCreationForm(data=driver_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, driver_data)

    def test_driver_license_update_form_with_validation(self):
        license_number = {
            "license_number": "YYY54321"
        }
        form = DriverLicenseUpdateForm(data=license_number)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, license_number)

    def test_driver_search_form_label(self):
        label = DriverSearchForm().fields["username"].label
        self.assertTrue(label == "" or label == "username")

    def test_driver_search_form_field_max_length(self):
        label = DriverSearchForm().fields["username"].max_length
        self.assertEqual(label, 63)


class CarFormTests(TestCase):
    def test_car_form_label(self):
        label = CarForm().fields["drivers"].label
        self.assertTrue(label is None or label == "username")

    def test_car_search_form_label(self):
        label = CarSearchForm().fields["model"].label
        self.assertTrue(label == "" or label == "model")

    def test_car_search_form_field_max_length(self):
        label = CarSearchForm().fields["model"].max_length
        self.assertEqual(label, 63)


class ManufacturerFormTests(TestCase):
    def test_manufacturer_search_form_label(self):
        label = ManufacturerSearchForm().fields["name"].label
        self.assertTrue(label == "" or label == "name")

    def test_manufacturer_search_form_field_max_length(self):
        label = ManufacturerSearchForm().fields["name"].max_length
        self.assertEqual(label, 63)
