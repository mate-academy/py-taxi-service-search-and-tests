from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm
)


class FormsTests(TestCase):
    def test_car_search_form_empty(self):
        form = CarSearchForm()
        self.assertEqual(form.fields["model"].label, "")

    def test_car_search_form_not_required(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test")

    def test_driver_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )

    def test_valid_license_number(self):
        form_data = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_empty(self):
        form = DriverSearchForm()
        self.assertEqual(form.fields["username"].label, "")

    def test_driver_search_form_not_required(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "test")

    def test_manufacturer_search_form_empty(self):
        form = ManufacturerSearchForm()
        self.assertEqual(form.fields["name"].label, "")

    def test_manufacturer_search_form_not_required(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test")
