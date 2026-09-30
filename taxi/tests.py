from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from taxi.forms import validate_license_number
from taxi.models import Car, Manufacturer


class LicenseValidationTests(TestCase):
    def test_valid_license_number(self):
        result = validate_license_number("ABC12345")
        self.assertEqual(result, "ABC12345")

    def test_license_number_wrong_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC123")

    def test_license_number_first_three_not_uppercase(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_license_number_last_five_not_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234A")


class PublicAccessTests(TestCase):
    def test_index_login_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        Car.objects.create(
            model="Camry", manufacturer=self.manufacturer1
        )
        Car.objects.create(
            model="X5", manufacturer=self.manufacturer2
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toy"}
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Cam"}
        )
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "X5")

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "testuser"}
        )
        self.assertContains(response, "testuser")


class VisitCounterTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="visitor",
            password="testpass123",
            license_number="XYZ98765",
        )
        self.client.force_login(self.user)

    def test_visit_counter_increases(self):
        self.client.get(reverse("taxi:index"))
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 2)
