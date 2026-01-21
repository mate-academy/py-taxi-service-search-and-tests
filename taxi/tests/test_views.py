from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.core.exceptions import ValidationError


from taxi.models import Driver, Car, Manufacturer
from taxi.forms import validate_license_number


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="testuser",
            password="12345"
        )
        self.client.force_login(self.user)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_toggle_assign_to_car(self):
        car_id = 1
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": car_id})
        )
        self.assertEqual(response.status_code, 404)


class CarListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.car1 = Car.objects.create(
            model="Toyota Camry", manufacturer=self.manufacturer1
        )

    def test_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"search": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota Camry")


class ManufacturerListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"search": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")


class LicenseNumberValidationTestCase(TestCase):
    def test_valid_license_number(self):
        valid_license_number = "ABC12345"
        result = validate_license_number(valid_license_number)
        self.assertEqual(result, valid_license_number)

    def test_invalid_length(self):
        invalid_license_number = "ABC1234"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_first_three_chars(self):
        invalid_license_number = "123AB567"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_last_five_chars(self):
        invalid_license_number = "ABCDEF12"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)

    def test_invalid_first_three_chars_not_uppercase(self):
        invalid_license_number = "abc12345"
        with self.assertRaises(ValidationError):
            validate_license_number(invalid_license_number)
