from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm


class ValidLicenseNumberFormTests(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_validation_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("DAF12345").is_valid())

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertFalse(self.create_form("ABC123456").is_valid())

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertFalse(self.create_form("RAF1234").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("FA123456").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("ABCD2345").is_valid())


class UpdateDriverLicenseNumberTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_update_driver_license_number_with_valid_data(self):
        test_license_number = "ADM22345"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 302)

    def test_update_driver_license_number_with_not_valid_data(self):
        test_license_number = "a5"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 200)
