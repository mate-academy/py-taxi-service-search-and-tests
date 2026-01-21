from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import (
    CarForm,
    CarSearchForm,
    validate_license_number,
    ManufacturerSearchForm,
    DriverSearchForm,
    DriverLicenseUpdateForm,
    DriverCreationForm,
)
from taxi.models import Manufacturer, Car


class CarTestForm(TestCase):

    def test_form_is_valid(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
            email="<EMAIL>",
        )
        manufacturer = Manufacturer.objects.create(
            country="testCountry",
            name="testName",
        )
        car = Car.objects.create(
            model="testModel",
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])
        form_data = {
            "model": "testModel",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id],
        }

        form = CarForm(data=form_data)
        self.assertEqual(form.is_valid(), True)


class CarSearchFormTest(TestCase):

    def test_form_is_valid(self):
        form_data = {
            "model": "Corolla",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Corolla")

    def test_form_has_placeholder(self):
        form = CarSearchForm()
        self.assertIn("placeholder", form.fields["model"].widget.attrs)
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"], "search by model"
        )


class ValidateLicenseNumberTest(TestCase):

    def test_valid_license_number(self):
        valid_license = "AAA11111"
        result = validate_license_number(valid_license)
        self.assertEqual(result, valid_license)

    def test_invalid_length(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("1111")
        self.assertEqual(
            str(context.exception),
            "['License number should consist of 8 characters']"
        )

    def test_invalid_uppercase(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("aaa11111")
        self.assertEqual(
            str(context.exception),
            "['First 3 characters should be uppercase letters']"
        )

    def test_invalid_digits(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("AAA11BB1")
        self.assertEqual(
            str(context.exception), "['Last 5 characters should be digits']"
        )


class ManufacturerFormTest(TestCase):
    def test_form_is_valid(self):
        form_data = {
            "name": "Test Manufacturer",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "testuser",
            "password1": "Password123ror",
            "password2": "Password123ror",
            "license_number": "AAA11111",
            "first_name": "Name",
            "last_name": "Surname",
            "email": "email@email.com",
        }

    def test_form_is_valid_with_valid_data(self):
        form = DriverCreationForm(data=self.form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_with_invalid_license_number(self):
        self.form_data["license_number"] = "AAA1"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):

    def test_form_is_valid_with_valid_data(self):
        driver = get_user_model().objects.create_user(
            username="testuser",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        form_data = {
            "license_number": "AAA11111",
        }
        form = DriverLicenseUpdateForm(instance=driver, data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_with_invalid_license_number(self):
        driver = get_user_model().objects.create_user(
            username="testuser",
            license_number="AAA11111",
            first_name="John",
            last_name="Doe",
        )
        form_data = {
            "license_number": "AA111",
        }
        form = DriverLicenseUpdateForm(instance=driver, data=form_data)
        self.assertFalse(form.is_valid())


class DriverSearchFormTest(TestCase):

    def test_form_is_valid_with_valid_username(self):
        form_data = {
            "username": "testuser",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
