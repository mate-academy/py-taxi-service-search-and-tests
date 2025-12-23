from django.test import TestCase
from taxi.forms import SearchForm, CarForm, DriverCreationForm
from taxi.models import Car, Manufacturer, Driver


class TestForms(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        cls.driver = Driver.objects.create_user(
            username="driver1",
            password="password",
            license_number="ABC12345"
        )
        cls.car = Car.objects.create(
            model="Camry",
            manufacturer=cls.manufacturer
        )
        cls.car.drivers.add(cls.driver)

        cls.driver_data = {
            "username": "testuser",
            "password1": "Testpassword123",
            "password2": "Testpassword123",
            "license_number": "XYZ67890",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_driver_creation_form_with_license_number(self):
        form = DriverCreationForm(data=self.driver_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            self.driver_data["license_number"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            self.driver_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            self.driver_data["last_name"]
        )

    def test_driver_creation_form_invalid_license_number(self):
        invalid_data = self.driver_data.copy()
        invalid_data["license_number"] = "abc123"

        form = DriverCreationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
