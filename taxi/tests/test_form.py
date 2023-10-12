from django import forms
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    CarSearchForm
)


class TestForm(TestCase):
    def test_driver_with_license_number_is_valid(self):
        data = {
            "username": "test",
            "password1": "A$test1234",
            "password2": "A$test1234",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "license_number": "AAA12345",
        }

        form = DriverCreationForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, data)

    def test_driver_with_invalid_license_number(self):
        data = {
            "username": "test",
            "password1": "A$test1234",
            "password2": "A$test1234",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "license_number": "aaa12345",
        }

        form = DriverCreationForm(data=data)

        self.assertFalse(form.is_valid())

    def test_driver_search_form_label_field(self):
        form = DriverSearchForm()
        self.assertEquals(form.fields["username"].label, "")

    def test_driver_search_form_required_field(self):
        form = DriverSearchForm()
        self.assertTrue(form.fields["username"].required)

    def test_manufacturer_search_form_max_length(self):
        form = ManufacturerSearchForm()
        self.assertEquals(form.fields["name"].max_length, 255)

    def test_car_search_form_widget_placeholder_exist(self):
        form = CarSearchForm()
        widget = form.fields["model"].widget
        self.assertTrue(
            widget.__dict__["attrs"]["placeholder"]
        )
