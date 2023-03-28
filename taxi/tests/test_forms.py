from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer
# from taxi.views


class LicenseNumberTests(TestCase):

    def test_license_number_should_have_all_caps(self) -> None:
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABa12422"}
        )

        self.assertFalse(form.is_valid())

    def test_license_number_should_have_five_digits(self) -> None:
        form = DriverLicenseUpdateForm(
            data={"license_number": "BBB1234"}
        )

        self.assertFalse(form.is_valid())

    def test_license_number_with_valid_data(self) -> None:
        form = DriverLicenseUpdateForm(
            data={"license_number": "CDA41312"}
        )

        self.assertTrue(form.is_valid())


class DriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "tester",
            "tespass234"
        )
        self.client.force_login(self.user)

    def test_create_driver(self) -> None:
        data = {
            "username": "dirvertest",
            "first_name": "First",
            "last_name": "Lasts",
            "license_number": "CAD25252",
            "password1": "drivepass22",
            "password2": "drivepass22",
        }
        respos = self.client.post(reverse("taxi:driver-create"), data=data)
        test_driver = get_user_model().objects.get(username=data["username"])

        self.assertEqual(test_driver.last_name, data["last_name"])
        self.assertEqual(test_driver.first_name, data["first_name"])
        self.assertEqual(test_driver.license_number, data["license_number"])
        self.assertEqual(respos.status_code, 302)
