from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormTest(TestCase):
    def test_driver_creation_form_with_license_number(self):
        form_date = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=form_date)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_date)

    def test_driver_licence_update(self):
        form_data = {
            "license_number": "TES12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_validate_license_number_less_8_characters(self):
        form_data = {
            "license_number": "TES1234",
        }
        DriverLicenseUpdateForm(data=form_data)
        self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters"
        )

    def test_driver_validate_license_number_not_starts_with_3_letters(self):
        form_datas = {
            "license_number": "TE123456",
            "license_number1": "TEs12345",
            "license_number2": "tes12345",
        }
        for form_data in form_datas:
            DriverLicenseUpdateForm(data=form_data)
            self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
            )

    def test_driver_validate_license_number_not_consists_5_last_digits(self):
        form_datas = {
            "license_number": "TESF3456",
            "license_number1": "TES1234G",
            "license_number2": "TES12r45",
        }
        for form_data in form_datas:
            DriverLicenseUpdateForm(data=form_data)
            self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits"
            )


class DriverSearchFormTests(TestCase):
    def test_renew_form_username_max_length(self):
        form = DriverSearchForm()
        self.assertTrue(
            form.fields["username"].max_length == 255
        )

    def test_renew_form_username_required(self):
        form = DriverSearchForm()
        self.assertTrue(
            form.fields["username"].required is False
        )

    def test_renew_form_username_label(self):
        form = DriverSearchForm()
        self.assertTrue(
            form.fields["username"].label == ""
        )

    def test_renew_form_username_widget(self):
        form = DriverSearchForm()
        self.assertTrue(
            form.fields["username"].widget.attrs["placeholder"]
            == "Search by username"
        )


class CarSearchFormTests(TestCase):
    def test_renew_form_model_max_length(self):
        form = CarSearchForm()
        self.assertTrue(
            form.fields["model"].max_length == 255
        )

    def test_renew_form_model_required(self):
        form = CarSearchForm()
        self.assertTrue(
            form.fields["model"].required is False
        )

    def test_renew_form_model_label(self):
        form = CarSearchForm()
        self.assertTrue(
            form.fields["model"].label == ""
        )

    def test_renew_form_model_widget(self):
        form = CarSearchForm()
        self.assertTrue(
            form.fields["model"].widget.attrs["placeholder"]
            == "Search by model"
        )


class ManufacturerSearchFormTests(TestCase):
    def test_renew_form_name_max_length(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].max_length == 255
        )

    def test_renew_form_name_required(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].required is False
        )

    def test_renew_form_name_label(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].label == ""
        )

    def test_renew_form_name_widget(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].widget.attrs["placeholder"]
            == "Search by name"
        )
