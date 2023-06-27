from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class DriverFormTest(TestCase):
    """tests for drivers forms"""
    def test_driver_creation_form_is_valid(self):
        """test driver creation form"""
        form_data = {
            "username": "new_user",
            "license_number": "PJH12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "password1": "user123test",
            "password2": "user123test",

        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_form_is_valid(self):
        """test driver license update form"""
        form_data = {"license_number": "PJH12345"}

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_licence_form_invalid_validation(self):
        """"test is invalid driver creation dorm"""
        invalid_license_number = [
            "zxc12345", "123ZC123", "12345678", "ASD123"
        ]
        for number in invalid_license_number:
            with self.subTest(license_number=number):
                form_data = {
                    "username": "test_user",
                    "password1": "password_test123",
                    "password2": "password_test123",
                    "first_name": "Test first",
                    "last_name": "Test last",
                    "license_number": number,
                }
                form = DriverCreationForm(data=form_data)
                self.assertFalse(form.is_valid())
                self.assertNotEqual(form.cleaned_data, form_data)


class CarFormTests(TestCase):
    """test to car forms"""
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="testik", country="test"
        )

        self.driver = get_user_model().objects.create_user(
            username="user_test",
            password="test2134",
            first_name="Test first",
            last_name="Test last",
            license_number="TES12345",
        )
        self.client.force_login(self.driver)

    def test_car_creation_form(self):
        """test car creation form"""
        car = {
            "model": "test",
            "manufacturer": self.manufacturer.id,
            "drivers": self.driver.id,
        }

        response = self.client.post(reverse("taxi:car-create"), car)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Car.objects.get(model="test").manufacturer.id, car["manufacturer"]
        )
        self.assertEqual(Car.objects.get(model="test").model, car["model"])
