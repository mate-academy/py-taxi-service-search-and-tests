from django.test import TestCase

from taxi.forms import DriverCreationForm, CarForm
from taxi.models import Manufacturer, Driver


class TestDriver(TestCase):
    def test_driver_creation_form_with_license_is_valid(self):
        form_data = {
            "license_number": "ABC51234",
            "username": "username",
            "password1": "Strong_password52",
            "password2": "Strong_password52",
            "first_name": "first_name",
            "last_name": "last_name"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TestCarForms(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_car_form_valid_data(self):
        driver = Driver.objects.create(
            username="driver1",
            password="pass123",
            first_name="Driver",
            last_name="One",
            license_number="ABC12345"
        )
        form_data = {
            "model": "Prius",
            "manufacturer": self.manufacturer.id,
            "drivers": [driver.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["model"],
            form_data["model"]
        )
