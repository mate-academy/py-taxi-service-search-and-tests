from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)
from taxi.models import Manufacturer, Car


class DriverFormsTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        valid_license_number = "TCA01010"
        form_data = {
            "username": "user",
            "password1": "userpassword",
            "password2": "userpassword",
            "first_name": "user_first",
            "last_name": "user_last",
            "license_number": valid_license_number
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creationg_form_with_invalid_data(self):
        invalid_license_number = "TC0101012"
        form_data_invalid = {
            "username": "user",
            "password1": "userpassword",
            "password2": "userpassword",
            "first_name": "user_first",
            "last_name": "user_last",
            "license_number": invalid_license_number
        }

        form_invalid = DriverCreationForm(data=form_data_invalid)
        self.assertFalse(form_invalid.is_valid())


class SearchFormsTests(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="FCA",
            country="Italy"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="driverpassword1",
            license_number="TCA00001"

        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="driverpassword2",
            license_number="TCA00002"
        )

        self.car1 = Car.objects.create(
            model="Car1",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Car2",
            manufacturer=self.manufacturer2
        )

        self.driver1.cars.add(self.car1)
        self.driver2.cars.add(self.car2)

    def test_manufacturer_search_form(self):
        form_data = {"name": "FCA"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        queryset = Manufacturer.objects.filter(name=form.cleaned_data["name"])
        self.assertQuerysetEqual(queryset, [self.manufacturer1])

    def test_car_search_form(self):
        form_data = {"model": "Car1"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        queryset = Car.objects.filter(model=form.cleaned_data["model"])
        self.assertQuerysetEqual(queryset, [self.car1])

    def test_driver_search_form(self):
        form_data = {"username": "driver1"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        queryset = get_user_model().objects.filter(
            username=form.cleaned_data["username"]
        )
        self.assertQuerysetEqual(queryset, [self.driver1])
