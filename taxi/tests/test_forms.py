from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import DriverCreationForm, CarForm
from taxi.models import Manufacturer


class FormTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "test123321",
            "password2": "test123321",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "AAA12345"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_creation_form_is_valid(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="UKR"
        )
        driver = get_user_model().objects.create(
            username="test1",
            password="test123",
            license_number="AAA12345"
        )
        drivers = get_user_model().objects.filter(id=driver.id)
        form_data = {
            "model": "test",
            "manufacturer": manufacturer,
            "drivers": drivers
        }

        form = CarForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(str(form.cleaned_data), str(form_data))
