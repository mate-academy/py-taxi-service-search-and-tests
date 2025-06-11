from django.test import TestCase
from taxi.forms import (
    CarForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm
)
from taxi.models import Manufacturer, Driver


class CarFormTest(TestCase):
    def test_car_form_is_valid(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        driver = Driver.objects.create_user(
            username="Test Driver",
            password="test1234",
            license_number="TEST1234",
        )
        form_data = {
            "model": "test_model",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id, ],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], form_data["model"])
        self.assertEqual(form.cleaned_data["manufacturer"], manufacturer)
        self.assertTrue(driver in form.cleaned_data["drivers"])

    def test_car_search_form_is_valid(self):
        form_data = {
            "model": "test_model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], form_data["model"])

    def test_car_search_form_field_placeholder(self):
        form = CarSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model"
        )


class ManufacturerFormTest(TestCase):
    def test_manufacturer_search_form_is_valid(self):
        form_data = {
            "name": "Test Manufacturer",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data["name"])

    def test_manufacturer_search_form_field_placeholder(self):
        form = ManufacturerSearchForm()
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name"
        )


class DriverFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_username",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TES12345",
        }

    def test_driver_create_form_is_valid(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            self.form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            self.form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            self.form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            self.form_data["license_number"]
        )

    def test_driver_create_form_with_invalid_license_number(self):
        self.form_data["license_number"] = "test1234124"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_driver_search_form_is_valid(self):
        form_data = {
            "username": "test_username",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])

    def test_driver_search_form_field_placeholder(self):
        form = DriverSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_is_valid(self):
        form_data = {
            "license_number": "TES12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )

    def test_driver_license_number_len_not_equal_to_8(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "test1234124",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_number_has_not_5_digits(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "tes1234",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_number_has_not_3_letters(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "te12345st",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
