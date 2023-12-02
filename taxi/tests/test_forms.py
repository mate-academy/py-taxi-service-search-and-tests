from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)


class ManufacturerSearchFormsTests(TestCase):
    def test_renew_form_name_field_max_length(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].max_length == 255)

    def test_renew_form_name_field_required(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].required is False)

    def test_renew_form_name_field_label(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].label is None
            or form.fields["name"].label == "")

    def test_renew_form_name_field_widget(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].widget.attrs["placeholder"]
            == "Search by name"
        )


class CarSearchFormsTests(TestCase):
    def test_renew_form_model_field_max_length(self):
        form = CarSearchForm()
        self.assertTrue(
            form.fields["model"].max_length == 255)

    def test_renew_form_model_field_required(self):
        form = CarSearchForm()
        self.assertTrue(
            form.fields["model"].required is False)

    def test_renew_form_model_field_label(self):
        form = CarSearchForm()
        self.assertTrue(
            form.fields["model"].label is None
            or form.fields["model"].label == ""
        )

    def test_renew_form_model_field_widget(self):
        form = CarSearchForm()
        self.assertTrue(
            form.fields["model"].widget.attrs["placeholder"]
            == "Search by model"
        )


class DriverSearchFormsTests(TestCase):
    def test_renew_form_username_field_max_length(self):
        form = DriverSearchForm()
        self.assertTrue(
            form.fields["username"].max_length == 255)

    def test_renew_form_username_field_required(self):
        form = DriverSearchForm()
        self.assertTrue(
            form.fields["username"].required is False)

    def test_renew_form_username_field_label(self):
        form = DriverSearchForm()
        self.assertTrue(
            form.fields["username"].label is None
            or form.fields["username"].label == ""
        )

    def test_renew_form_username_field_widget(self):
        form = DriverSearchForm()
        self.assertTrue(
            form.fields["username"].widget.attrs["placeholder"]
            == "Search by username"
        )


class DriverCreateFormsTests(TestCase):
    def test_renew_form_data_fields_label(self):
        form = DriverCreationForm()
        self.assertTrue(
            form.fields["license_number"].label == "License number")
        self.assertTrue(
            form.fields["first_name"].label == "First name")
        self.assertTrue(
            form.fields["last_name"].label == "Last name")

    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TST12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormsTests(TestCase):
    def test_license_number_is_valid(self):
        form_data = {
            "license_number": "TST12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())


class DriverLicenseValidationTests(TestCase):
    def test_license_number_is_not_valid_consist_less_8_characters(self):
        form_data = {
            "license_number": "TST1234",
        }
        DriverLicenseUpdateForm(data=form_data)
        self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters"
        )

    def test_license_number_not_first_3_characters_uppercase_letters(self):
        form_data_base = {
            "license_number1": "tST12345",
            "license_number2": "TsT12345",
            "license_number3": "TSt12345",
            "license_number4": "tst12345",
        }
        for form_data in form_data_base:
            DriverLicenseUpdateForm(data=form_data)
            self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
            )

    def test_license_number_is_not_consist_last_5_characters_is_digits(self):
        form_data_base = {
            "license_number1": "TSTA2345",
            "license_number2": "TST1A345",
            "license_number3": "TST12A45",
            "license_number4": "TST123A5",
            "license_number5": "TST1234A",
        }
        for form_data in form_data_base:
            DriverLicenseUpdateForm(data=form_data)
            self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits"
            )
