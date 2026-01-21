from django.test import TestCase

from taxi.forms import CarForm, DriverLicenseUpdateForm
from taxi.models import Driver, Manufacturer


class TestForm(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Fasd",
            country="asd"
        )
        self.driver1 = Driver.objects.create_user(
            username="Driver1",
            password="1234",
            license_number="TES12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="Driver2",
            password="1234",
            license_number="TES12341"
        )

    def test_valid_data_car(self):
        form_data = {
            "model": "Test10",
            "manufacturer": 1,
            "drivers": [1, 2]
        }
        form = CarForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_valid_data_driver(self):
        form_data = {
            "license_number": "TES22345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_invalid_data_car(self):
        form_data = {
            "model": 42,
            "manufacturer": "Manufacturer",
            "drivers": Driver.objects.filter(id__lt=3),
        }
        form = CarForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_invalid_nums_driver(self):
        form_data = {
            "license_number": "TES12345412"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_invalid_symbols_driver(self):
        form_data = {
            "license_number": "TE12345412"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_without_symbols_driver(self):
        form_data = {
            "license_number": "12345412"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
