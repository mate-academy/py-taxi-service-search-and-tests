from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, CarForm
from taxi.models import Manufacturer, Driver


class DriverFormTests(TestCase):
    def test_driver_creation_with_licence_number(self):
        form_data = {
            "username": "driver1",
            "license_number": "RET12345",
            "first_name": "Driver",
            "last_name": "Driver",
            "password1": "bjBhg/<s.GC$v`d6Pa?K8*",
            "password2": "bjBhg/<s.GC$v`d6Pa?K8*"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CarFormTests(TestCase):
    def test_car_form_creation(self):
        manufacturer = Manufacturer.objects.create(name="test", country="USA")
        driver = get_user_model().objects.create(
            username="test",
            password="test123",
        )
        form_data = {
            "model": "TestForm Model",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
