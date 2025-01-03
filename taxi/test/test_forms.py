from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm,\
    DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class FormsDriverTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "Strongpassword123",
            "password2": "Strongpassword123",
            "first_name": "New",
            "last_name": "User",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_license_number_form_is_valid(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form_valid_with_data(self):
        form_data = {"username": "test"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form_valid_with_empty_data(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form_has_placeholder(self):
        form = DriverSearchForm()
        self.assertIn("placeholder", form["username"].field.widget.attrs)
        self.assertEqual(
            form["username"].field.widget.attrs["placeholder"],
            "Search for drivers"
        )


class FormsCarTest(TestCase):
    def test_car_search_form_valid_with_data(self):
        form_data = {"model": "test"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form_valid_with_empty_data(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form_has_placeholder(self):
        form = CarSearchForm()
        self.assertIn("placeholder", form["model"].field.widget.attrs)
        self.assertEqual(
            form["model"].field.widget.attrs["placeholder"],
            "Search for cars"
        )


class FormsManufacturerTest(TestCase):
    def test_manufacturer_search_form_valid_with_data(self):
        form_data = {"name": "test"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form_valid_with_empty_data(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form_has_placeholder(self):
        form = ManufacturerSearchForm()
        self.assertIn("placeholder", form["name"].field.widget.attrs)
        self.assertEqual(
            form["name"].field.widget.attrs["placeholder"],
            "Search for manufacturers"
        )
