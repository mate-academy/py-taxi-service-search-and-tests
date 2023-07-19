from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm
)
from taxi.models import Manufacturer, Car


class FormsTests(TestCase):
    def test_driver_create_form_with_licence_first_last_name_is_valid(
            self
    ) -> None:
        form_data = {
            "username": "TestDriver",
            "password1": "test123456",
            "password2": "test123456",
            "first_name": "TestFirst",
            "last_name": "TestLast",
            "license_number": "TES12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_number(self) -> None:
        form_data = {
            "license_number": "12345678"
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class SearchForm(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="author123456",
            license_number="BBB12345",
        )

        self.client.force_login(self.user)

    def test_search_form_car(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TEST"
        )
        Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Other",
            manufacturer=manufacturer
        )

        form_data = {
            "model": "TestMod"
        }

        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        expected_result = Car.objects.filter(model="TestModel")

        response = self.client.get(
            reverse("taxi:car-list") + "?model=" + form_data["model"]
        )
        self.assertEqual(
            list(response.context["car_list"]), list(expected_result)
        )

    def test_search_form_manufacture(self) -> None:
        Manufacturer.objects.create(
            name="TestManufacturer",
            country="TEST"
        )

        Manufacturer.objects.create(
            name="Other",
            country="USA"
        )

        form_data = {
            "name": "Test"
        }

        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        expected_result = Manufacturer.objects.filter(name="TestManufacturer")

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=" + form_data["name"]
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(expected_result)
        )

    def test_search_form_driver(self) -> None:
        get_user_model().objects.create_user(
            username="TestUser",
            password="author123456",
            license_number="BBB12346",
        )
        get_user_model().objects.create_user(
            username="OtherUser",
            password="author123456",
            license_number="BBB12347",
        )

        form_data = {
            "username": "Test"
        }

        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        expected_result = get_user_model().objects.filter(username="TestUser")

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=" + form_data["username"]
        )
        self.assertEqual(
            list(response.context["driver_list"]), list(expected_result)
        )
