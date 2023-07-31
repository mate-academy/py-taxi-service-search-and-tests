from django.test import TestCase

from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="testpassword",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="testpassword",
            license_number="XYZ67890"
        )
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")

    def test_car_form_valid(self):
        form_data = {
            "manufacturer": self.manufacturer1.id,
            "model": "Camry",
            "year": 2020,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            "make": "Toyota",
            "model": "Camry",
            "year": 2020,
            "drivers": [],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "new_driver",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number(self):
        form_data = {
            "username": "new_driver",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC123456",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="testpassword"
        )

    def test_driver_license_update_form_valid(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form_data = {
            "license_number": "ABC123456",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
