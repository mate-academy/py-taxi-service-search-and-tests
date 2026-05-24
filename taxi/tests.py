from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Manufacturer, Car
from taxi.forms import validate_license_number


class SearchFeaturesTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="password123",
            license_number="ADM11111"
        )
        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create_user(
            username="alex_driver",
            password="123",
            license_number="DRV22222"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="bob_taxi",
            password="123",
            license_number="DRV33333"
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer2
        )

    def test_search_driver_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "alex"})

        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertNotIn(self.driver2, response.context["driver_list"])

    def test_search_car_by_model_case_insensitive(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "CAMRY"})

        self.assertIn(self.car1, response.context["car_list"])
        self.assertNotIn(self.car2, response.context["car_list"])

    def test_search_manufacturer_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Ford"})

        self.assertIn(
            self.manufacturer2,
            response.context["manufacturer_list"]
        )
        self.assertNotIn(
            self.manufacturer1,
            response.context["manufacturer_list"]
        )


class CoreFeatureValidationTest(TestCase):
    def test_valid_license_number(self):
        valid_number = "XYZ98765"
        self.assertEqual(validate_license_number(valid_number), valid_number)

    def test_license_number_wrong_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123456")

    def test_license_number_first_three_not_uppercase_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")
        with self.assertRaises(ValidationError):
            validate_license_number("AB112345")

    def test_license_number_last_five_not_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234X")
