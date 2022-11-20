from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class FormsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="testik", country="test"
        )

        self.driver = get_user_model().objects.create_user(
            username="user",
            password="password_test123",
            first_name="Test first",
            last_name="Test last",
            license_number="TJK12345",
        )
        self.client.force_login(self.driver)

    def test_driver_creation_form_with_valid_license(self):
        form_data = {
            "username": "test_user",
            "password1": "password_test123",
            "password2": "password_test123",
            "license_number": "TOK12345",
            "first_name": "Test first",
            "last_name": "Test last",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_invalid_license(self):
        invalid_license = [
            "TJK123",
            "tjk12345",
            "12345",
        ]

        for license_ in invalid_license:
            with self.subTest(license_number=license_):
                form_data = {
                    "username": "test_user",
                    "password1": "password_test123",
                    "password2": "password_test123",
                    "first_name": "Test first",
                    "last_name": "Test last",
                    "license_number": license_,
                }

                form = DriverCreationForm(data=form_data)
                self.assertFalse(form.is_valid())
                self.assertNotEqual(form.cleaned_data, form_data)

    def test_driver_update_form_with_valid_license(self):
        form_data = {
            "license_number": "TOK12345",
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_form_with_invalid_license(self):
        invalid_license = [
            "TJK123",
            "tjk12345",
            "12345",
        ]

        for license_ in invalid_license:
            with self.subTest(license_number=license_):
                form_data = {
                    "license_number": license_,
                }

                form = DriverLicenseUpdateForm(data=form_data)
                self.assertFalse(form.is_valid())
                self.assertNotEqual(form.cleaned_data, form_data)

    def test_car_creation_form(self):
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
