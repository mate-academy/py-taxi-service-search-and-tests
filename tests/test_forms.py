from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class FormTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_user",
            "password1": "OceanCode712@",
            "password2": "OceanCode712@",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )

    def test_driver_license_update_form(self):
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )

    def test_driver_license_update_form_with_invalid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "1234567890"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "license_number": [
                    "License number should consist of 8 characters"
                ]
            }
        )
        form2 = DriverLicenseUpdateForm(data={"license_number": "abc12345"})
        self.assertFalse(form2.is_valid())
        self.assertEqual(
            form2.errors,
            {
                "license_number": [
                    "First 3 characters should be uppercase letters"
                ]
            }
        )
        form3 = DriverLicenseUpdateForm(data={"license_number": "ABCDEFGH"})
        self.assertFalse(form3.is_valid())
        self.assertEqual(
            form3.errors,
            {
                "license_number": [
                    "Last 5 characters should be digits"
                ]
            }
        )


class DriverSearchFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.user)
        self.driver1 = get_user_model().objects.create_user(
            username="test_user1",
            password="pass",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="test_user2",
            password="pass",
            license_number="ABC12346"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="other_user",
            password="pass",
            license_number="ABC12347"
        )

    def test_driver_search_form_returns_correct_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test"}
        )
        self.assertEqual(response.status_code, 200)

        drivers = list(response.context["driver_list"])
        self.assertIn(self.driver1, drivers)
        self.assertIn(self.driver2, drivers)
        self.assertNotIn(self.driver3, drivers)


class CarSearchFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.user)
        self.car1 = Car.objects.create(
            model="Test Car",
            manufacturer=Manufacturer.objects.create(
                name="Test Manufacturer",
                country="Test Country"
            )
        )
        self.car2 = Car.objects.create(
            model="Test Car 2",
            manufacturer=Manufacturer.objects.create(
                name="Test Manufacturer 2",
                country="Test Country 2"
            )
        )
        self.car3 = Car.objects.create(
            model="Other Car",
            manufacturer=Manufacturer.objects.create(
                name="Other Manufacturer",
                country="Other Country"
            )
        )

    def test_car_search_form_returns_correct_results(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "Test"})
        self.assertEqual(response.status_code, 200)
        cars = list(response.context["car_list"])
        self.assertIn(self.car1, cars)
        self.assertIn(self.car2, cars)
        self.assertNotIn(self.car3, cars)


class ManufacturerSearchFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Other Manufacturer",
            country="Other Country"
        )

    def test_manufacturer_search_form_returns_correct_results(self):
        response = self.client.get(
            reverse(
                "taxi:manufacturer-list"
            ),
            {"name": "Test"}
        )
        self.assertEqual(response.status_code, 200)
        manufacturers = list(response.context["manufacturer_list"])
        self.assertIn(self.manufacturer1, manufacturers)
        self.assertIn(self.manufacturer2, manufacturers)
        self.assertNotIn(self.manufacturer3, manufacturers)
