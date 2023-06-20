from django.forms import CheckboxSelectMultiple
from django.test import TestCase

from taxi import forms


class SearchFormsTest(TestCase):
    def setUp(self):
        self.car = forms.CarSearchForm()
        self.driver = forms.DriverSearchForm()
        self.manufacturer = forms.ManufacturerSearchForm()

    def test_search_form_labels(self):
        """Tests that search form labels are empty"""
        self.assertEqual(self.car.fields["model"].label, "")
        self.assertEqual(self.driver.fields["username"].label, "")
        self.assertEqual(self.manufacturer.fields["name"].label, "")

    def test_search_form_placeholders(self):
        """Tests that search form placeholders are in correct format"""
        for form, field in {
            self.car: "model",
            self.driver: "username",
            self.manufacturer: "name",
        }.items():
            self.assertEqual(
                form.fields[field].widget.attrs["placeholder"],
                f"Search by {field}..."
            )


class CarFormTest(TestCase):
    def test_car_form_drivers_field_widget(self):
        """Tests that driver field widget is set to CheckboxSelectMultiple"""
        form = forms.CarForm()

        self.assertTrue(
            isinstance(
                form.fields["drivers"].widget, CheckboxSelectMultiple
            )
        )


class DriverFormTest(TestCase):
    def test_driver_creation_form_with_additional_fields_is_valid(self):
        form_data = {
            "username": "charlie",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "Charlie",
            "last_name": "Smith",
            "license_number": "DHS37272",
        }
        form = forms.DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseNumberUpdateValidationTest(TestCase):
    """Tests license number validation"""
    @staticmethod
    def init_form(license_number):
        return forms.DriverLicenseUpdateForm(
            data={"license_number": license_number}
        )

    def test_license_number_with_valid_data(self):
        self.assertTrue(self.init_form("KDS74321").is_valid())

    def test_license_number_should_not_be_longer_than_8_characters(self):
        self.assertFalse(self.init_form("ABC123456").is_valid())

    def test_license_number_should_not_be_shorter_than_8_characters(self):
        self.assertFalse(self.init_form("ABC1234").is_valid())

    def test_license_number_first_3_chars_should_be_uppercase_letters(self):
        self.assertFalse(self.init_form("sdj32392").is_valid())
        self.assertFalse(self.init_form("sD392091").is_valid())

    def test_license_number_last_5_chars_should_be_digits(self):
        self.assertFalse(self.init_form("CDM32A39").is_valid())
