from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.forms import (DriverCreationForm,
                        DriverSearchForm,
                        ManufacturerSearchForm,
                        CarSearchForm)
from taxi.models import Manufacturer, Car


class FormTests(TestCase):
    def test_driver_create_with_valid_data(self) -> None:
        form_data = {
            "username": "TestDriver",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "license_number": "TST12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class SearchForm(TestCase):
    def __init__(self, methodname: str = ...):
        super().__init__(methodname)
        self.client = None

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="author12345",
            license_number="ABC12345",
        )

        self.client.force_login(self.user)

    def test_search_form_car(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="Test"
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
            country="Test"
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
            password="author12345",
            license_number="ABC12346",
        )
        get_user_model().objects.create_user(
            username="OtherUser",
            password="author123456",
            license_number="ABC12347",
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
