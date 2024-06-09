from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    ManufacturerNameSearchForm,
    DriverUsernameSearchForm,
    CarModelSearchForm,
)


class FormsTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "license_number": "TES12345",
            "first_name": "Test_name",
            "last_name": "Test_last_name",
        }

    def get_form(self, **kwargs):
        form_data = self.form_data.copy()
        form_data.update(kwargs)
        return DriverCreationForm(data=form_data)

    def test_driver_creation_form(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_valid_license_number(self):
        form = self.get_form(license_number="TES12348")
        self.assertTrue(form.is_valid())


class SearchFormsTests(TestCase):

    def test_driver_search_form_valid(self):
        form_data = {"username": "test.user"}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test.user")

    def test_driver_search_form_empty(self):
        form_data = {"username": ""}
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_car_search_form_valid(self):
        form_data = {"model": "test.model"}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test.model")

    def test_car_search_form_empty(self):
        form_data = {"model": ""}
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_manufacturer_search_form_valid(self):
        form_data = {"name": "test.name"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test.name")

    def test_manufacturer_search_form_empty(self):
        form_data = {"name": ""}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")
