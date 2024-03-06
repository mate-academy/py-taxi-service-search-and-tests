from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarForm,
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)

from taxi.models import Manufacturer


class FormTests(TestCase):
    def test_form_validity(self):
        form_data = {
            "username": "new_user",
            "password1": "testing123new",
            "password2": "testing123new",
            "license_number": "ABC12345",
            "first_name": "Test_first_name",
            "last_name": "Test_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, form_data)

    def test_update_license_number(self):
        new_license_form = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=new_license_form)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, new_license_form)


class CarSearchFormTest(TestCase):

    def test_form_validation(self):
        form_valid = CarSearchForm(data={"model": "Toyota"})
        self.assertTrue(form_valid.is_valid())


class ManufacturerSearchFormTest(TestCase):

    def test_form_validation(self):
        form = ManufacturerSearchForm(data={"name": "BMW"})
        self.assertTrue(form.is_valid())


class DriverSearchFormTest(TestCase):

    def test_form_validation(self):
        form_valid = DriverSearchForm(
            data={
                "username": "admin1",
                "license_number": "ABC12345"
            }
        )
        self.assertTrue(form_valid.is_valid())


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.driver1 = get_user_model().objects.create(
            username="John",
            license_number="NKG65214"
        )
        self.driver2 = get_user_model().objects.create(
            username="Alice",
            license_number="NKL65204"
        )

    def test_car_form_is_valid(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_is_not_valid(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
