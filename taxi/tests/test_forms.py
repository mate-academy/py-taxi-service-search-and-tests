from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm
)


class DriverCreationFormTest(TestCase):
    @staticmethod
    def get_form_data() -> dict:
        return {
            "username": "papajoe",
            "password1": "$ecreT_550",
            "password2": "$ecreT_550",
        }

    def test_driver_creation_form_valid_license(self):
        form_data = self.get_form_data()
        form_data["license_number"] = "MAN99901"
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_no_license(self):
        form_data = self.get_form_data()
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_license_incorrect_format(self):
        incorrect_licenses = ["man999", "MAN9999W", "mAN", "1244425f"]
        form_data = self.get_form_data()

        for incorrect_license in incorrect_licenses:
            form_data["license_number"] = incorrect_license
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())


class SearchFormsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="papajoe",
            password="$ecreT_550",
            license_number="MAN99901"
        )
        self.client.force_login(self.user)

    def test_empty_search_form_is_valid(self):
        field_form = {
            CarSearchForm: "model",
            ManufacturerSearchForm: "name",
            DriverSearchForm: "username"
        }
        for search_form, field in field_form.items():
            form_data = {
                field: "",
            }
            form = search_form(data=form_data)
            self.assertTrue(form.is_valid())
