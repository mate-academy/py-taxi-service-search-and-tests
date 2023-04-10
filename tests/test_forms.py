from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy


DRIVER_TEST_URL = reverse_lazy("taxi:driver-update", kwargs={"pk": 1})


class DriverLicenseValidationTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="ADM12345"
        )

        self.client.force_login(self.driver)

    def test_len_license_number(self):
        response = self.client.post(DRIVER_TEST_URL, data={"license_number": "ad123"})

        self.assertFormError(response, "form", "license_number", "License number should consist of 8 characters")

    def test_first_three_characters_uppercase(self):
        response = self.client.post(DRIVER_TEST_URL, data={"license_number": "aDM12345"})

        self.assertFormError(response, "form", "license_number", "First 3 characters should be uppercase letters")

    def test_first_three_characters_digit(self):
        response = self.client.post(DRIVER_TEST_URL, data={"license_number": "A1M12345"})

        self.assertFormError(response, "form", "license_number", "First 3 characters should be uppercase letters")

    def test_last_five_characters_are_digits(self):
        response = self.client.post(DRIVER_TEST_URL, data={"license_number": "ADM12a45"})

        self.assertFormError(response, "form", "license_number", "Last 5 characters should be digits")
