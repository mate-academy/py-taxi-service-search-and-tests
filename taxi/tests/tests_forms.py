from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormsTests(TestCase):
    def test_driver_creation_form_with_first_last_name_is_valid(self):
        form_data = {
            "username": "test_user",
            "password1": "pass123test",
            "password2": "pass123test",
            "first_name": "test",
            "last_name": "test",
            "license_number": "AAA12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverSearchFormTestCase(TestCase):
    def test_form_driver_valid(self):
        data = {"first_name": "test"}
        form = DriverSearchForm(data=data)
        self.assertTrue(form.is_valid)


class CarSearchFormTestCase(TestCase):
    def test_form_field_label(self):
        form = CarSearchForm()
        self.assertEqual(form.fields["model"].max_length, 255)

    def test_form_valid(self):
        data = {"model": "test"}
        form = CarSearchForm(data=data)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTestCase(TestCase):
    def test_form_manufacturer_valid(self):
        data = {"name": "test", "country": "test"}
        form = ManufacturerSearchForm(data=data)
        self.assertTrue(form.is_valid)
