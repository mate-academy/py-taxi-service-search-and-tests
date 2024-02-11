from django.test import TestCase

from taxi import forms
from taxi.forms import DriverCreationForm, CarSearchForm, ManufacturerSearchForm, DriverSearchForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AAA12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

class CarSearchFormTestCase(TestCase):
    def test_form_field_label(self):
        form = CarSearchForm()
        self.assertEqual(form.fields["model"].max_length, 15)


    def test_form_valid(self):
        data = {"model": "Test Model"}
        form = CarSearchForm(data=data)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTestCase(TestCase):
    def test_form_manufacturer_valid(self):
        data = {
            "name": "Test Name",
            "country": "Test Country"
        }
        form = ManufacturerSearchForm(data=data)
        self.assertTrue(form.is_valid)


class DriverSearchFormTestCase(TestCase):
    def test_form_driver_valid(self):
        data = {"first_name": "Test first name"}
        form = DriverSearchForm(data=data)
        self.assertTrue(form.is_valid)


