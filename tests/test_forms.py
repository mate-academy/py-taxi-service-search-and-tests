from django.test import TestCase
from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer, Driver


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.driver = Driver.objects.create_user(
            username="testuser", password="password"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "Corolla",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {"model": ""}
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_form_drivers_field(self):
        form = CarForm()
        self.assertIn("drivers", form.fields)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "supersecretpassword",
            "password2": "supersecretpassword",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number(self):
        form_data = {
            "username": "newdriver",
            "password1": "supersecretpassword",
            "password2": "supersecretpassword",
            "license_number": "INVALID",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_missing_first_name_allowed(self):
        form_data = {
            "username": "newdriver",
            "password1": "supersecretpassword",
            "password2": "supersecretpassword",
            "license_number": "ABC12345",
            "first_name": "",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_missing_last_name_allowed(self):
        form_data = {
            "username": "newdriver",
            "password1": "supersecretpassword",
            "password2": "supersecretpassword",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_update_form_valid(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_license_update_form_invalid(self):
        form_data = {"license_number": "INVALID"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_license_update_form_field_label(self):
        form = DriverLicenseUpdateForm()
        self.assertTrue(
            form.fields["license_number"].label is None
            or form.fields["license_number"].label == "License number"
        )
