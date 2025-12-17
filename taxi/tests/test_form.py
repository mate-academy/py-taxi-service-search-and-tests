from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriversUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerSearchForm,
    validate_license_number,
)
from taxi.models import Car, Manufacturer

User = get_user_model()


class FormsTestCase(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan"
                                                        )
        self.user = User.objects.create_user(username="testuser",
                                             password="password123",
                                             license_number="ABC12345"
                                             )
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer
                                      )
        self.car.drivers.add(self.user)

    def test_car_form_valid(self):
        form_data = {"model": "Corolla", "manufacturer": self.manufacturer.id,
                     "drivers": [self.user.id]}
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "driver1",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123",
            "license_number": "DEF67890",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "driver2",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123",
            "license_number": "def67890",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_license_update_form_invalid_length(self):
        form = DriverLicenseUpdateForm(instance=self.user,
                                       data={"license_number": "ABC1234"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_validate_license_number_raises(self):
        with self.assertRaises(ValidationError):
            validate_license_number("A1C12345")  # first 3 chars invalid

    def test_drivers_username_search_form(self):
        form = DriversUsernameSearchForm(data={"username": "testuser"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_car_model_search_form_empty_is_valid(self):
        form = CarModelSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"manufacturer": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["manufacturer"], "Toyota")
