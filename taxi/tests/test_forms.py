from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple
from django.test import TestCase

from taxi.forms import validate_license_number, DriverLicenseUpdateForm, DriverCreationForm, CarForm
from taxi.models import Manufacturer


class TestValidateLicenseNumber(TestCase):
    # <>= 8 chars in license
    def test_valid_license_number(self):
        result = validate_license_number("ABC12345")
        self.assertEqual(result, "ABC12345")

    def test_too_short_license_number(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_license_number("ABC12")
        self.assertIn("8 characters", str(ctx.exception))

    def test_too_long_license_number(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_license_number("ABC1234567890")
        self.assertIn("8 characters", str(ctx.exception))

    # first 3 uppercase letters and last 5 digits
    def test_digits_instead_letters_in_license_number(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_license_number("12412345")
        self.assertIn("First 3", str(ctx.exception))

    def test_lowercase_letters_in_license_number(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_license_number("abc12345")
        self.assertIn("First 3", str(ctx.exception))

    def test_letters_instead_digits_in_license_number(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_license_number("ABCsadff")
        self.assertIn("Last 5", str(ctx.exception))

class TestDriverUpdateForm(TestCase):
    #driver license update form
    def test_valid_driver_license_update_form(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABS12345"})
        self.assertTrue(form.is_valid())

    def test_invalid_driver_license_update_form(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AAAA242"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_empty_driver_license_update_form(self):
        form = DriverLicenseUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class TestDriverCreationForm(TestCase):
    def get_user_data(self):
        return {
            "username": "test_user",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "TES12345",
            "first_name": "test_first",
            "last_name": "test_last",
        }

    #valid form
    def test_driver_creation_with_valid_data(self):
        form = DriverCreationForm(data=self.get_user_data())
        self.assertTrue(form.is_valid())

    #invalid form
    def test_empty_data_driver_creation(self):
        form = DriverCreationForm(data={})
        self.assertFalse(form.is_valid())

    def test_invalid_license_number_driver_creation(self):
        data = self.get_user_data()
        data["license_number"] = "Dio_Brando"
        form = DriverCreationForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_in_fields_driver_creation(self):
        form = DriverCreationForm(data=self.get_user_data())

        self.assertIn("license_number", form.fields)

    def test_first_name_in_fields_driver_creation(self):
        form = DriverCreationForm(data=self.get_user_data())

        self.assertIn("first_name", form.fields)

    def test_last_name_in_fields_driver_creation(self):
        form = DriverCreationForm(data=self.get_user_data())

        self.assertIn("last_name", form.fields)

    def test_invalid_password_driver_creation(self):
        data = self.get_user_data()
        data["password2"] = "WRONG_PASSWORD"
        form = DriverCreationForm(data=data)

        self.assertFalse(form.is_valid())


class TestCarForm(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test_Manufacturer",
            country="Test_Country",
        )
        self.driver1 = get_user_model().objects.create_user(
            username="test_user1",
            password="test_password",
            license_number="TES11111",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="test_user2",
            password="test_password",
            license_number="TES22222",
        )

    def test_drivers_field_uses_checkbox_widget(self):
        form = CarForm()
        self.assertIsInstance(form.fields["drivers"].widget, CheckboxSelectMultiple)

    def test_drivers_field_uses_model_queryset(self):
        form = CarForm()
        queryset = form.fields["drivers"].queryset

        self.assertIn(self.driver1, queryset)
        self.assertIn(self.driver2, queryset)

    def test_valid_form_car_create(self):
        form = CarForm(data={
            "model":"Test_model",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk],
        })

        self.assertTrue(form.is_valid())

    def test_valid_form_with_empty_drivers_car_create(self):
        form = CarForm(data={
            "model":"Test_model",
            "manufacturer": self.manufacturer.pk,
            "drivers": [],
        })

        self.assertFalse(form.is_valid())
