from django import forms
from django.test import TestCase

from taxi.forms import DriverCreationForm, CarForm, CarSearchForm, DriverSearchForm, ManufacturerSearchForm, \
    DriverLicenseUpdateForm


class CarFormTest(TestCase):
    def test_car_drivers_user_widget_checkbox(self):
        form = CarForm()
        self.assertIsInstance(form.fields["drivers"].widget, forms.CheckboxSelectMultiple)

    def test_car_form_creation_with_all_fields(self):
        form = CarForm()
        self.assertEqual(list(form.fields.keys()), ["model", "manufacturer", "drivers"])


class CarSearchFormTest(TestCase):
    def setUp(self):
        self.form = CarSearchForm()

    def test_car_search_form_with_model_field(self):
        self.assertIn("model", self.form.fields)

    def test_car_search_form_model_field_label(self):
        self.assertEqual(self.form.fields["model"].label, "")

    def test_car_search_form_model_field_max_length(self):
        self.assertEqual(self.form.fields["model"].max_length, 255)

    def test_car_search_form_model_field_required(self):
        self.assertEqual(self.form.fields["model"].required, False)

    def test_car_search_form_model_field_widget_with_placeholder(self):
        self.assertIsInstance(self.form.fields["model"].widget, forms.TextInput)
        self.assertEqual(self.form.fields["model"].widget.attrs["placeholder"], "Model")


class DriverCreationFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_user",
            "password1": "Skdhsdf123",
            "password2": "Skdhsdf123",
            "first_name": "first",
            "last_name": "last",
        }

    def test_driver_creation_form_with_license_number_first_name_last_name(self):
        self.form_data["license_number"] = "ABC12345"
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_short_license_number(self):
        list_invalid_license_numbers = [
            "",
            "A",
            "AB12",
            "ABC1234",
        ]

        for license_number in list_invalid_license_numbers:
            self.form_data["license_number"] = license_number
            self.form = DriverCreationForm(data=self.form_data)
            self.assertFalse(self.form.is_valid())


    def test_driver_creation_form_with_long_license_number(self):
        self.form_data["license_number"] = "ABC123456"
        self.form = DriverCreationForm(data=self.form_data)
        self.assertFalse(self.form.is_valid())

    def test_driver_creation_form_license_number_first_3_letters_uppercase(self):
        list_invalid_license_numbers = [
            "abc12345",
            "AbC12345",
            "AB112345",
            "A_C12345",
            "AB 12345",
        ]

        for license_number in list_invalid_license_numbers:
            self.form_data["license_number"] = license_number
            self.form = DriverCreationForm(data=self.form_data)
            self.assertFalse(self.form.is_valid())

    def test_driver_creation_form_license_number_last_5_char_digits(self):
        list_invalid_license_numbers = [
            "ABC12A12",
            "ABC1234",
            "ABC12-45",
            "ABC 1234"
        ]

        for license_number in list_invalid_license_numbers:
            self.form_data["license_number"] = license_number
            self.form = DriverCreationForm(data=self.form_data)
            self.assertFalse(self.form.is_valid())



class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.form_data = {}

    def test_driver_license_update_form_with_license_number(self):
        self.form_data["license_number"] = "ABC12345"
        form = DriverLicenseUpdateForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_license_update_form_with_short_license_number(self):
        list_invalid_license_numbers = [
            "",
            "A",
            "AB12",
            "ABC1234",
        ]

        for license_number in list_invalid_license_numbers:
            self.form_data["license_number"] = license_number
            self.form = DriverLicenseUpdateForm(data=self.form_data)
            self.assertFalse(self.form.is_valid())


    def test_driver_license_update_form_with_long_license_number(self):
        self.form_data["license_number"] = "ABC123456"
        self.form = DriverLicenseUpdateForm(data=self.form_data)
        self.assertFalse(self.form.is_valid())

    def test_driver_license_update_form_license_number_first_3_letters_uppercase(self):
        list_invalid_license_numbers = [
            "abc12345",
            "AbC12345",
            "AB112345",
            "A_C12345",
            "AB 12345",
        ]

        for license_number in list_invalid_license_numbers:
            self.form_data["license_number"] = license_number
            self.form = DriverLicenseUpdateForm(data=self.form_data)
            self.assertFalse(self.form.is_valid())

    def test_driver_license_update_form_license_number_last_5_char_digits(self):
        list_invalid_license_numbers = [
            "ABC12A12",
            "ABC1234",
            "ABC12-45",
            "ABC 1234"
        ]

        for license_number in list_invalid_license_numbers:
            self.form_data["license_number"] = license_number
            self.form = DriverLicenseUpdateForm(data=self.form_data)
            self.assertFalse(self.form.is_valid())


class DriverSearchFormTest(TestCase):
    def setUp(self):
        self.form = DriverSearchForm()

    def test_driver_search_form_with_username_field(self):
        self.assertIn("username", self.form.fields)

    def test_driver_search_form_username_field_label(self):
        self.assertEqual(self.form.fields["username"].label, "")

    def test_driver_search_form_username_field_max_length(self):
        self.assertEqual(self.form.fields["username"].max_length, 150)

    def test_driver_search_form_username_field_required(self):
        self.assertEqual(self.form.fields["username"].required, False)

    def test_driver_search_form_username_field_widget_with_placeholder(self):
        self.assertIsInstance(self.form.fields["username"].widget, forms.TextInput)
        self.assertEqual(self.form.fields["username"].widget.attrs["placeholder"], "Username")


class ManufacturerSearchFormTest(TestCase):
    def setUp(self):
        self.form = ManufacturerSearchForm()

    def test_manufacturer_search_form_with_name_field(self):
        self.assertIn("name", self.form.fields)

    def test_manufacturer_search_form_name_field_label(self):
        self.assertEqual(self.form.fields["name"].label, "")

    def test_manufacturer_search_form_name_field_max_length(self):
        self.assertEqual(self.form.fields["name"].max_length, 255)

    def test_manufacturer_search_form_name_field_required(self):
        self.assertEqual(self.form.fields["name"].required, False)

    def test_manufacturer_search_form_name_field_widget_with_placeholder(self):
        self.assertIsInstance(self.form.fields["name"].widget, forms.TextInput)
        self.assertEqual(self.form.fields["name"].widget.attrs["placeholder"], "Name")