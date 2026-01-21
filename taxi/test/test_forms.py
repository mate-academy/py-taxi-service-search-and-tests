from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    fixtures = ["taxi_service_db_data.json"]

    def test_drivers_field_is_checkboxselectmultiple(self):
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        )

    def test_car_creation_form_is_valid(self):
        data = {
            "model": "test_model",
            "manufacturer": 1,
            "drivers": [1]
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], data["model"])
        self.assertEqual(
            form.cleaned_data["manufacturer"],
            Manufacturer.objects.get(pk=data["manufacturer"])
        )
        self.assertEqual(
            list(form.cleaned_data["drivers"]),
            list(get_user_model().objects.filter(pk__in=data["drivers"]))
        )


class DriverCreationFormTest(TestCase):
    def test_form_has_all_fields_specified(self):
        form = DriverCreationForm()
        expected_fields = [
            "username",
            "license_number",
            "first_name",
            "last_name",
            "password1",
            "password2"
        ]
        self.assertEqual(
            list(form.fields.keys()),
            expected_fields
        )

    def test_driver_creation_form_is_valid(self):
        data = {
            "username": "new_user",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_driver_creation_form_is_not_valid(self):
        data = {
            "username": "new_user",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "ABC",
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_form_has_all_fields_specified(self):
        form = DriverLicenseUpdateForm()
        expected_fields = ["license_number"]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_driver_license_update_form_is_valid(self):
        form = DriverLicenseUpdateForm({"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")

    def test_driver_license_update_form_is_not_valid(self):
        form = DriverLicenseUpdateForm({"license_number": "ABC"})
        self.assertFalse(form.is_valid())
