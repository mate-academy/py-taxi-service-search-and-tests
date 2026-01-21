from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriversUsernameSearchForm,
    CarsModelSearchForm,
    ManufacturerNameSearchForm,
)
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        self.driver = get_user_model().objects.create_user(
            username="test_user", password="test123"
        )

    def test_form_is_valid(self):
        data = {
            "model": "test_model",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_form_is_valid(self):
        data = {
            "username": "test_user",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TST12345",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_license_number(self):
        data = {
            "username": "test_user",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TST",
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "License number should consist of 8 characters"
        )

        data = {
            "username": "test_user",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TESTTEST",
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form, "license_number", "Last 5 characters should be digits"
        )

        data = {
            "username": "test_user",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "tst12345",
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "First 3 characters should be uppercase letters"
        )


class DriverLicenseUpdateFormTest(TestCase):
    def test_form_is_valid(self):
        data = {
            "license_number": "TST12345",
        }
        form = DriverLicenseUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_license_number(self):
        data = {
            "license_number": "TST123",
        }
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "License number should consist of 8 characters"
        )

        data = {
            "license_number": "TEST1234",
        }
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "Last 5 characters should be digits"
        )

        data = {
            "license_number": "tst12345",
        }
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "license_number",
            "First 3 characters should be uppercase letters"
        )


class DriversUsernameSearchFormTest(TestCase):
    def test_form_is_valid(self):
        form = DriversUsernameSearchForm(data={"username": "test_user"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test_user")

    def test_form_valid_without_username(self):
        form = DriversUsernameSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_form_field_attributes(self):
        form = DriversUsernameSearchForm()
        username_field = form.fields["username"]
        self.assertEqual(username_field.max_length, 255)
        self.assertFalse(username_field.required)
        self.assertEqual(username_field.label, "")
        self.assertEqual(
            username_field.widget.attrs.get("placeholder"),
            "Search by Username"
        )


class CarsModelSearchFormTest(TestCase):
    def test_form_is_valid(self):
        form = CarsModelSearchForm(data={"model": "test_model"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test_model")

    def test_form_valid_without_model(self):
        form = CarsModelSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_form_field_attributes(self):
        form = CarsModelSearchForm()
        model_field = form.fields["model"]
        self.assertEqual(model_field.max_length, 255)
        self.assertFalse(model_field.required)
        self.assertEqual(model_field.label, "")
        self.assertEqual(
            model_field.widget.attrs.get("placeholder"),
            "Search by Model"
        )


class ManufacturerNameSearchFormTest(TestCase):
    def test_form_is_valid(self):
        form = ManufacturerNameSearchForm(data={"name": "test_name"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test_name")

    def test_form_valid_without_name(self):
        form = ManufacturerNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_form_field_attributes(self):
        form = ManufacturerNameSearchForm()
        name_field = form.fields["name"]
        self.assertEqual(name_field.max_length, 255)
        self.assertFalse(name_field.required)
        self.assertEqual(name_field.label, "")
        self.assertEqual(
            name_field.widget.attrs.get("placeholder"),
            "Search by Name"
        )
