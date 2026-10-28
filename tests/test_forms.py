from django.test import TestCase
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchField
)
from taxi.models import Car, Driver


class CarFormTest(TestCase):
    def test_drivers_label(self):
        form = CarForm()
        self.assertTrue(
            form.fields["drivers"].label is None
            or form.fields["drivers"].label == "drivers"
        )

    def test_checking_for_model(self):
        form = CarForm()
        self.assertTrue(
            form.Meta.model == Car
        )

    def test_checking_for_fields(self):
        form = CarForm()
        self.assertIn(
            "model", form.fields
        )
        self.assertIn("manufacturer", form.fields)
        self.assertIn("drivers", form.fields)


class DriverCreationFormTest(TestCase):
    def test_model_of_form(self):
        form = DriverCreationForm()
        self.assertTrue(form.Meta.model == Driver)


class DriverLicenseUpdateFormTest(TestCase):
    def test_model_of_form(self):
        form = DriverLicenseUpdateForm()
        self.assertTrue(form.Meta.model == Driver)

    def test_validate_license_number_function(self):
        form_1 = DriverLicenseUpdateForm(data={"license_number": "ABCC12345"})
        form_2 = DriverLicenseUpdateForm(data={"license_number": "ABCDEFGI"})
        form_3 = DriverLicenseUpdateForm(data={"license_number": "abc12345"})

        self.assertFalse(form_1.is_valid())
        self.assertFalse(form_2.is_valid())
        self.assertFalse(form_3.is_valid())


class DriverSearchFormTest(TestCase):
    def test_search_field_placeholder(self):
        form = DriverSearchForm()

        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Enter driver's name..."
        )
        self.assertEqual(form.fields["username"].label, "")


class CarSearchFormTest(TestCase):
    def test_search_field_placeholder(self):
        form = CarSearchForm()

        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Enter car model..."
        )


class ManufacturerSearchFieldTest(TestCase):
    def test_search_field_placeholder(self):
        form = ManufacturerSearchField()

        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Enter manufacturer name..."
        )
