from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


DRIVER_UPDATE_URL = reverse("taxi:driver-update", kwargs={"pk": 1})


class LicenseValidationTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test username",
            password="test123",
            license_number="TST12345"
        )

        self.client.force_login(self.driver)

    def test_len_license_number(self):
        response = self.client.post(DRIVER_UPDATE_URL, data={"license_number": "TST1234"})

        self.assertFormError(response, "form", "license_number", "License number should consist of 8 characters")

    def test_first_three_characters_uppercase(self):
        response = self.client.post(DRIVER_UPDATE_URL, data={"license_number": "tst12345"})

        self.assertFormError(response, "form", "license_number", "First 3 characters should be uppercase letters")

    def test_first_three_characters_letters(self):
        response = self.client.post(DRIVER_UPDATE_URL, data={"license_number": "1ST12345"})

        self.assertFormError(response, "form", "license_number", "First 3 characters should be uppercase letters")

    def test_last_five_characters_digits(self):
        response = self.client.post(DRIVER_UPDATE_URL, data={"license_number": "TST123a5"})

        self.assertFormError(response, "form", "license_number", "Last 5 characters should be digits")


class SearchFormsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Porsche", country="Germany"
        )

        self.driver = get_user_model().objects.create_user(
            username="test username",
            password="test123",
            first_name="test first",
            last_name="test last",
            license_number="TST12345"
        )

        self.car = Car.objects.create(
            model="Porsche 911", manufacturer=self.manufacturer
        )

    def test_drivers_search_username(self):
        response = self.client.get(reverse("taxi:driver-list") + "?username=test username")

        self.assertFalse("Bob" in str(response.content))

    def test_cars_search_porsche_911(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Porsche 911")

        self.assertFalse("Toyota Yaris" in str(response.content))

    def test_manufacturers_search_porsche(self):
        response = self.client.get(reverse("taxi:manufacturer-list") + "?name=Porsche")

        self.assertFalse("BMW" in str(response.content))


