from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturersSearchForm,
    CarSearchForm,
    DriverSearchForm
)


class FormTest(TestCase):
    def test_author_create_with_clean_license_number_is_valid(self):
        form_data = {
            "username": "testusername",
            "first_name": "First name Test",
            "last_name": "Last name Test",
            "password1": "123testadmin!QW",
            "password2": "123testadmin!QW",
            "license_number": "AAA11111"
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.clean_license_number())
        self.assertEqual(
            form.clean_license_number(),
            form_data["license_number"]
        )

    def test_author_update_with_clean_license_number_is_valid(self):
        form_data = {
            "license_number": "AAA11111"
        }

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.clean_license_number())
        self.assertEqual(
            form.clean_license_number(),
            form_data["license_number"]
        )

    def test_search_driver_is_valid(self):
        form_data = {
            "empty": {"title": ""},
            "not_empty": {"title": "abc"}
        }

        form_empty = DriverSearchForm(form_data["empty"])
        form_not_empty = DriverSearchForm(form_data["not_empty"])

        self.assertTrue(form_empty.is_valid())
        self.assertTrue(form_not_empty.is_valid())
        self.assertEqual(
            form_empty.fields["title"].widget.attrs["placeholder"],
            "Search by name:"
        )

    def test_search_car_is_valid(self):
        form_data = {
            "empty": {"title": ""},
            "not_empty": {"title": "abc"}
        }

        form_empty = CarSearchForm(form_data["empty"])
        form_not_empty = CarSearchForm(form_data["not_empty"])

        self.assertTrue(form_empty.is_valid())
        self.assertTrue(form_not_empty.is_valid())
        self.assertEqual(
            form_empty.fields["title"].widget.attrs["placeholder"],
            "Search by name:"
        )

    def test_search_manufacturer_form_is_valid(self):
        form_data = {
            "empty": {"title": ""},
            "not_empty": {"title": "abc"}
        }

        form_empty = ManufacturersSearchForm(form_data["empty"])
        form_not_empty = ManufacturersSearchForm(form_data["not_empty"])

        self.assertTrue(form_empty.is_valid())
        self.assertTrue(form_not_empty.is_valid())
        self.assertEqual(
            form_empty.fields["title"].widget.attrs["placeholder"],
            "Search by name:"
        )
