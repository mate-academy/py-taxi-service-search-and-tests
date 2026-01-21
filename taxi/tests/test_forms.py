from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    validate_license_number,
    ManufacturerListSearchForm,
    DriverListSearchForm,
    CarListSearchForm,
)
from taxi.models import Car, Manufacturer, Driver


class CarFormTest(TestCase):
    def test_car_form_fields(self):
        form = CarForm()

        self.assertIn("drivers", form.fields)

        self.assertTrue(
            isinstance(form.fields["drivers"], forms.ModelMultipleChoiceField)
        )

        self.assertTrue(
            isinstance(form.fields["drivers"].widget,
                       forms.CheckboxSelectMultiple)
        )

        expected_queryset = get_user_model().objects.all()
        self.assertQuerysetEqual(
            form.fields["drivers"].queryset, map(repr, expected_queryset)
        )

    def test_creation_form(self):
        form = DriverCreationForm()

        expected_fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )
        self.assertListEqual(list(form._meta.fields), list(expected_fields))

    def test_driver_creation_form_license_number_validation(self):
        invalid_license_numbers = [
            "ABC123456",
            "12345678rrrrr",
            "AD569842",
        ]

        for license_number in invalid_license_numbers:
            form_data = {
                "username": "test_user",
                "password1": "testDriver123",
                "password2": "testDriver123",
                "license_number": license_number,
                "first_name": "Test",
                "last_name": "User",
            }
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid(), form.errors)

        valid_license_numbers = ["ADM56984", "JOY26458", "JIM26531"]

        for license_number in valid_license_numbers:
            form_data = {
                "username": "test_user",
                "password1": "testDriver123",
                "password2": "testDriver123",
                "license_number": license_number,
                "first_name": "Test",
                "last_name": "User",
            }
            form = DriverCreationForm(data=form_data)
            self.assertTrue(form.is_valid(), form.errors)

    def test_driver_license_update_form(self):
        invalid_license_numbers = [
            "ABC123456",
            "12345678rrrrr",
            "AD3M56984",
        ]
        for license_number in invalid_license_numbers:
            form_data = {"license_number": license_number}
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid(), form.errors)

    def test_car_list_search_form(self):
        form = CarListSearchForm()
        self.assertTrue("model" in form.fields)
        self.assertTrue(form.fields["model"].required is False)

        self.assertTrue(form.fields["model"].widget.attrs["placeholder"])

    def test_driver_list_search_form(self):
        form = DriverListSearchForm()
        self.assertTrue("username" in form.fields)
        self.assertTrue(form.fields["username"].required is False)

        self.assertTrue(form.fields["username"].widget.attrs["placeholder"])

    def test_manufacturer_list_search_form(self):
        form = ManufacturerListSearchForm()
        self.assertTrue("name" in form.fields)
        self.assertTrue(form.fields["name"].required is False)

        self.assertTrue(form.fields["name"].widget.attrs["placeholder"])
