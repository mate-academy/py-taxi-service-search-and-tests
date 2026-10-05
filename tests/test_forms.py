from django.test import TestCase
from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Driver


class DriverDataTest(TestCase):
    def make_form(self, license_number):
        return DriverCreationForm(data={
            "username": "testdriver",
            "password1": "A-strong-test-password-123!",
            "password2": "A-strong-test-password-123!",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": license_number,
        })

    def test_accept_valid_data(self):
        form = self.make_form("ABC12345")
        self.assertTrue(form.is_valid())

    def test_reject_invalid_license_number_length(self):
        form = self.make_form("ABC1234")
        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_reject_lowercase_letters_in_license_number(self):
        form = self.make_form("abc12345")
        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_reject_non_letters_in_license_prefix(self):
        form = self.make_form("AB112345")
        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_reject_non_digits_in_license_number(self):
        form = self.make_form("ABC12D45")
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"]
        )

    def test_accept_valid_license_update(self):
        form = DriverLicenseUpdateForm(data={
            "license_number": "XYZ67890"
        })
        self.assertTrue(form.is_valid())

    def test_reject_invalid_license_update(self):
        form = DriverLicenseUpdateForm(data={
            "license_number": "XYZ6789"
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )


class CarFormTest(TestCase):
    def test_valid_data_saves_car_and_selected_drivers(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        driver = Driver.objects.create_user(
            username="testdriver",
            password="A-strong-test-password-123!",
            license_number="ABC12345"
        )

        form = CarForm(data={
            "model": "Corolla",
            "manufacturer": manufacturer.pk,
            "drivers": [driver.pk]
        })
        self.assertTrue(form.is_valid(), form.errors)

        car = form.save()

        self.assertEqual(car.model, "Corolla")
        self.assertEqual(car.manufacturer, manufacturer)
        self.assertIn(driver, car.drivers.all())
