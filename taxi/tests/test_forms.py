from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from taxi.forms import (CarForm,
                        CarSearchForm,
                        DriverCreationForm,
                        DriverLicenseUpdateForm,
                        DriverSearchForm,
                        ManufacturerSearchForm,
                        validate_license_number
                        )
from taxi.models import (Car,
                         Driver,
                         Manufacturer)

User = get_user_model()


class CarFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        cls.driver1 = User.objects.create_user(
            username="driver1",
            password="password1",
            license_number="ABC12345"
        )
        cls.driver2 = User.objects.create_user(
            username="driver2",
            password="password2",
            license_number="DEF67890"
        )

    def test_car_form_valid_data(self):
        form = CarForm(data={
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id]
        })
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_data(self):
        form = CarForm(data={"model": "", "manufacturer": "", "drivers": []})
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)
        self.assertIn("manufacturer", form.errors)


class CarSearchFormTest(TestCase):
    def test_car_search_form_valid_data(self):
        form = CarSearchForm(data={"car": "Camry"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["car"], "Camry")

    def test_car_search_form_empty_data(self):
        form = CarSearchForm(data={"car": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["car"], "")


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid_data(self):
        form = DriverCreationForm(data={
            "username": "driver3",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe"
        })
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number(self):
        form = DriverCreationForm(data={
            "username": "driver4",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "license_number": "1234ABC",
            "first_name": "Jane",
            "last_name": "Smith"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid_data(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12345"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"], "ABC12345"
        )

    def test_driver_license_update_form_invalid_data(self):
        form = DriverLicenseUpdateForm(data={"license_number": "1234"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_valid_data(self):
        form = DriverSearchForm(data={"driver": "driver1"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["driver"], "driver1")

    def test_driver_search_form_empty_data(self):
        form = DriverSearchForm(data={"driver": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["driver"], "")


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_valid_data(self):
        form = ManufacturerSearchForm(data={"manufacturer": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["manufacturer"], "Toyota"
        )

    def test_manufacturer_search_form_empty_data(self):
        form = ManufacturerSearchForm(data={"manufacturer": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["manufacturer"], "")


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(
            validate_license_number("ABC12345"), "ABC12345"
        )

    def test_license_number_invalid_length(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("AB1234")
        (self.assertIn
         ("License number should consist of 8 characters",
          str(context.exception))
         )

    def test_license_number_invalid_letters(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("A1C12345")
        (self.assertIn
         ("First 3 characters should be uppercase letters",
          str(context.exception))
         )

    def test_license_number_invalid_digits(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC1234A")
        (self.assertIn
         ("Last 5 characters should be digits", str(context.exception))
         )
