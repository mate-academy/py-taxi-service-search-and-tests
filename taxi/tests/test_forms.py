from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, CarForm
from taxi.models import Manufacturer, Car


class FormsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="KJS95721"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test name",
            country="test country",
        )
        self.car = Car.objects.create(
            model="test model",
            manufacturer=self.manufacturer
        )

    def test_car_form(self):
        form_data = {
            "model": "test model",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.cleaned_data["drivers"]), [self.user])
        self.assertEqual(form.cleaned_data["manufacturer"], self.manufacturer)
        self.assertEqual(form.cleaned_data["model"], form_data["model"])

    def test_driver_creation_form(self):
        form_data = {
            "username": "new_river",
            "password1": "Test123Driver",
            "password2": "Test123Driver",
            "license_number": "VLA64930",
            "first_name": "Firstname",
            "last_name": "Lastname"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )
