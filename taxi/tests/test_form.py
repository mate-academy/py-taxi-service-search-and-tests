from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriversSearchForm,
    CarsSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Driver, Car, Manufacturer


class FormsTest(TestCase):
    def setUp(self):
        self.manufacturer1 = (
            Manufacturer.objects.create(
                name="test",
                country="testcountry"
            )
        )
        self.manufacturer2 = (
            Manufacturer.objects.create(
                name="another",
                country="anothercountry"
            )
        )

        self.car1 = (
            Car.objects.create(
                model="test",
                manufacturer=self.manufacturer1
            )
        )
        self.car2 = (
            Car.objects.create(
                model="another",
                manufacturer=self.manufacturer2
            )
        )

        self.driver1 = (
            Driver.objects.create_user(
                username="testuser",
                password="pass12345",
                license_number="ABC12345"
            )
        )
        self.driver2 = (
            Driver.objects.create_user(
                username="another",
                password="pass12345",
                license_number="XYZ56789"
            )
        )

    def test_driver_creation_form_license_number_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_drivers_search_form(self):
        form_data = {"username": "testuser"}
        form = DriversSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")
        result = (
            Driver.objects.filter(
                username__icontains=form.cleaned_data["username"]
            )
        )
        self.assertIn(self.driver1, result)
        self.assertNotIn(self.driver2, result)

    def test_car_search_form(self):
        form_data = {"model": "test"}
        form = CarsSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test")
        results = (
            Car.objects.filter(
                model__icontains=form.cleaned_data["model"]
            )
        )
        self.assertIn(self.car1, results)
        self.assertNotIn(self.car2, results)

    def test_manufacturer_search_form(self):
        form_data = {"name": "test"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "test")
        results = (
            Manufacturer.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        )
        self.assertIn(self.manufacturer1, results)
        self.assertNotIn(self.manufacturer2, results)
