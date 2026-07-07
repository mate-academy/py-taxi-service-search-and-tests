from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm
)


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_and_name(self):
        form_data = {
            "username": "gandalf",
            "password1": "test123!",
            "password2": "test123!",
            "first_name": "Gandalf",
            "last_name": "The Grey",
            "license_number": "ZXC09876",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_form_with_license(self):
        form_data = {
            "license_number": "XSW00009"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form_is_not_empty(self):
        form_data = {
            "name": "Volvo",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form_is_empty(self):
        form_data = {
            "name": "Volvo",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form_empty(self):
        form_data = {
            "name": "",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_from_label_and_placeholder(self):
        form = ManufacturerSearchForm()
        self.assertEqual(form.fields["name"].label, "")
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name"
        )

    def test_car_search_form_is_not_empty(self):
        form_data = {
            "model": "Q5",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form_is_empty(self):
        form_data = {
            "model": ""
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_from_label_and_placeholder(self):
        form = CarSearchForm()
        self.assertEqual(form.fields["model"].label, "")
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model"
        )

    def test_driver_search_form_is_not_empty(self):
        form_data = {
            "username": "frodo_torba",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form_is_empty(self):
        form_data = {
            "username": ""
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_from_label_and_placeholder(self):
        form = DriverSearchForm()
        self.assertEqual(form.fields["username"].label, "")
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )
