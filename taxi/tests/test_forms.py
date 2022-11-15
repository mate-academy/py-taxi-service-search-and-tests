from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer, Driver


class ManufacturerFormsTest(TestCase):
    def test_manufacturer_search_form(self):
        form_data = {"name": "tester"}
        form = ManufacturerSearchForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CarFormsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.driver1 = Driver.objects.create(
            username="test1", password="password123", license_number="ASD12345"
        )
        self.driver2 = Driver.objects.create(
            username="test2", password="password123", license_number="ASD12346"
        )

    def test_car_creation_form(self):
        form_data = {
            "model": "model",
            "manufacturer": self.manufacturer,
            "drivers": [self.driver1, self.driver2]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.cleaned_data), list(form_data))

    def test_car_search_form(self):
        form_data = {"model": "tester"}
        form = CarSearchForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverFormTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create(
            username="test", password="password1234", license_number="ASD12345"
        )

    def test_driver_creation_form_license_first_last_name_valid(self):
        form_data = {
            "username": "username1",
            "license_number": "ASD12349",
            "first_name": "first",
            "last_name": "last",
            "password1": "Kdsa12eMda23",
            "password2": "Kdsa12eMda23",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(list(form.cleaned_data), list(form_data))

    def test_driver_creation_form_wrong_license_first_last_name_valid(self):
        form_data = {
            "username": "username1",
            "license_number": "AD1349",
            "first_name": "first",
            "last_name": "last",
            "password1": "Kdsa12eMda23",
            "password2": "Kdsa12eMda23",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_update_correct_license(self):
        form = DriverLicenseUpdateForm({"license_number": "QWE12345"})
        self.assertTrue(form.is_valid())

    def test_driver_update_wrong_license(self):
        license_list = [
            "As123456", "ASd12345", "1DD12345", "ASDF1234", "ASDF12345"
        ]
        for license_ in license_list:
            form = DriverLicenseUpdateForm({"license_number": license_})
            self.assertFalse(form.is_valid())

    def test_driver_search_form(self):
        form_data = {"username": "tester"}
        form = DriverSearchForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

