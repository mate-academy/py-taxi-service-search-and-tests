from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car

User = get_user_model()


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_custom_license_validation(self):
        """Test custom validation for license number in DriverCreationForm."""
        form = DriverCreationForm(data={
            "username": "newuser",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "A1B2C3D4"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_valid_license(self):
        """Test valid license number in DriverCreationForm."""
        form = DriverCreationForm(data={
            "username": "newuser",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345"
        })
        self.assertTrue(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_custom_validation(self):
        """
        Test custom validation for
        license number in DriverLicenseUpdateForm.
        """
        form = DriverLicenseUpdateForm(data={
            "license_number": "12345678"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_valid_license(self):
        """Test valid license number in DriverLicenseUpdateForm."""
        form = DriverLicenseUpdateForm(data={
            "license_number": "XYZ12345"
        })
        self.assertTrue(form.is_valid())


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver1 = User.objects.create_user(
            username="driver1",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.driver2 = User.objects.create_user(
            username="driver2",
            password="password123",
            first_name="Jane",
            last_name="Doe",
            license_number="XYZ12345"
        )

    def test_car_form_valid_data(self):
        """Test valid data for CarForm including multiple drivers."""
        form = CarForm(data={
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id]
        })
        self.assertTrue(form.is_valid())

    def test_car_form_missing_manufacturer(self):
        """Test CarForm with missing manufacturer."""
        form = CarForm(data={
            "model": "Corolla",
            "manufacturer": "",
            "drivers": [self.driver1.id]
        })
        self.assertFalse(form.is_valid())
        self.assertIn("manufacturer", form.errors)
