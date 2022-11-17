from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverSearchForm, CarSearchForm
from taxi.models import Driver, Car, Manufacturer


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        data = {
            "username": "test",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_driver_search_form_valid_data(self):
        driver = Driver.objects.create(
            username="test",
            license_number="FRE12345"
        )
        data = {
            "driver_0": driver.username
        }
        form = DriverSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid_data(self):
        manufacturer = Manufacturer.objects.create(name="test")
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        data = {
            "car_0": car.model
        }
        form = CarSearchForm(data=data)
        self.assertTrue(form.is_valid())
