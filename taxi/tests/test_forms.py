from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm
)
from taxi.models import Car, Manufacturer, Driver

User = get_user_model()


class CarFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="driver1",
            password="12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "X5",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_drivers_checkbox(self):
        form = CarForm()
        self.assertIn("drivers", form.fields)
        self.assertEqual(
            form.fields["drivers"].widget.__class__.__name__,
            "CheckboxSelectMultiple"
        )


class DriverCreationFormTests(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "abc12345",  # invalid
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="12345",
            license_number="ABC12345"
        )

    def test_license_update_valid(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "XYZ54321"},
            instance=self.driver
        )
        self.assertTrue(form.is_valid())

    def test_license_update_invalid_length(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12"},
            instance=self.driver
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_update_invalid_letters(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "abC12345"},
            instance=self.driver
        )
        self.assertFalse(form.is_valid())

    def test_license_update_invalid_digits(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC12D45"},
            instance=self.driver
        )
        self.assertFalse(form.is_valid())
