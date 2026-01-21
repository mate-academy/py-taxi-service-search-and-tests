from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import Manufacturer


class FormsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota", country="japan")
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="PASSWORD",
            license_number="XYZ543212",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="PASSWORD2",
            license_number="XYZ54321",
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "car",
            "manufacturer": self.manufacturer.pk,
            "driver": self.driver1.pk,
        }
        form = CarForm(data=form_data)
        if not form.is_valid():
            self.fail(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "PASSWORD",
            "password2": "PASSWORD",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        if not form.is_valid():
            self.fail(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XYZ54321"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_valid(self):
        form = DriverSearchForm(data={"username": "John"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form = ManufacturerSearchForm(data={"name": "ZAZ"})
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid(self):
        form = CarSearchForm(data={"model": "car"})
        self.assertTrue(form.is_valid())
