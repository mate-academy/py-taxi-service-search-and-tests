from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class DriverFormsTest(TestCase):
    def test_driver_creation_with_lisence_first_last_name_is_valid(
            self
    ) -> None:
        form_data = {
            "username": "Test",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "FirstName",
            "last_name": "LastName",
            "license_number": "TRE12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_consists_of_8_characters_while_creating_driver(
            self
    ) -> None:
        form = DriverCreationForm(data={"license_number": "TRY1234567"})
        form1 = DriverCreationForm(data={"license_number": "TR567"})

        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"],
        )
        self.assertEqual(
            form1.errors["license_number"],
            ["License number should consist of 8 characters"],
        )

    def test_license_number_first_3_letters_uppercase_while_creating_driver(
            self
    ) -> None:
        form = DriverCreationForm(data={"license_number": "dFg12345"})
        form1 = DriverCreationForm(data={"license_number": "DF112345"})

        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"],
        )
        self.assertEqual(
            form1.errors["license_number"],
            ["First 3 characters should be uppercase letters"],
        )

    def test_license_number_last_5_characters_digits_while_creating_driver(
            self
    ) -> None:
        form = DriverCreationForm(data={"license_number": "FGT1234T"})
        form1 = DriverCreationForm(data={"license_number": "FGTR1234"})

        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )
        self.assertEqual(
            form1.errors["license_number"],
            ["Last 5 characters should be digits"]
        )

    def test_driver_updating_lisence_number_is_valid(self) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "TRE12345"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {"license_number": "TRE12345"})

    def test_license_number_consists_of_8_characters_while_its_updating(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TRY1234567"})
        form1 = DriverLicenseUpdateForm(data={"license_number": "TR567"})

        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"],
        )
        self.assertEqual(
            form1.errors["license_number"],
            ["License number should consist of 8 characters"],
        )

    def test_license_number_first_3_letters_uppercase_while_its_updating(self):
        form = DriverLicenseUpdateForm(data={"license_number": "dFg12345"})
        form1 = DriverLicenseUpdateForm(data={"license_number": "DF112345"})

        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"],
        )
        self.assertEqual(
            form1.errors["license_number"],
            ["First 3 characters should be uppercase letters"],
        )

    def test_license_number_last_5_characters_digits_while_its_updating(self):
        form = DriverLicenseUpdateForm(data={"license_number": "FGT1234T"})
        form1 = DriverLicenseUpdateForm(data={"license_number": "FGTR1234"})

        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )
        self.assertEqual(
            form1.errors["license_number"],
            ["Last 5 characters should be digits"]
        )

    def test_driver_search_label_empty(self):
        form = DriverSearchForm()
        self.assertTrue(form.fields["username"].label == "")

    def test_driver_search_placeholder_text(self):
        form = DriverSearchForm()
        self.assertTrue(
            form.fields["username"].
            widget.attrs["placeholder"] == "search by username"
        )


class CarFormsTest(TestCase):
    def test_car_search_label_empty(self):
        form = CarSearchForm()
        self.assertTrue(form.fields["model"].label == "")

    def test_car_search_placeholder_text(self):
        form = CarSearchForm()
        self.assertTrue(
            form.fields["model"].widget.
            attrs["placeholder"] == "search by model"
        )


class ManufacturerFormsTest(TestCase):
    def test_manufacturer_search_label_empty(self):
        form = ManufacturerSearchForm()
        self.assertTrue(form.fields["name"].label == "")

    def test_manufacturer_search_placeholder_text(self):
        form = ManufacturerSearchForm()
        self.assertTrue(
            form.fields["name"].widget.attrs["placeholder"] == "search by name"
        )
