from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarForm,
    CarSearchForm,
    DriverSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm,
)
from taxi.models import Manufacturer, Car


class FormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Nissan", country="Japan"
        )
        self.driver = get_user_model().objects.create_user(
            username="driver1", password="test123", license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2", password="test321", license_number="DRV12345"
        )
        self.car1 = Car.objects.create(
            model="Skyline", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Altima", manufacturer=self.manufacturer
        )

    def test_car_form_valid_data(self):
        form_data = {
            "model": "Skyline",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_results(self):
        form = ManufacturerSearchForm(data={"name": "Nissan"})
        self.assertTrue(form.is_valid())
        results = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertIn(self.manufacturer, results)

    def test_driver_creation_form_with_all_data_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "TST12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(
            form.cleaned_data["license_number"], form_data["license_number"]
        )

    def test_valid_license_number_update(self):
        form_data = {"license_number": "TST12345"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"], form_data["license_number"]
        )

    def test_car_search_form_valid_data(self):
        form = CarSearchForm(data={"model": "Skyline"})
        self.assertTrue(form.is_valid())
        results = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertIn(self.car1, results)

    def test_car_search_form_invalid_data(self):
        form = CarSearchForm(data={"model": "Civic"})
        self.assertTrue(form.is_valid())
        results = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertNotIn(self.car1, results)

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Nissan"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "driver1"})
        self.assertTrue(form.is_valid())

    def test_driver_search_results(self):
        form = DriverSearchForm(data={"username": "driver1"})
        self.assertTrue(form.is_valid())
        results = get_user_model().objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertIn(self.driver, results)

    def test_driver_search_results_not_contains(self):
        form = DriverSearchForm(data={"username": "driver3"})
        self.assertTrue(form.is_valid())
        results = get_user_model().objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertNotIn(self.driver, results)
