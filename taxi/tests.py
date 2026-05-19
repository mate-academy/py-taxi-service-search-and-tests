from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicTests(TestCase):
    """Test that non-authenticated users cannot access core lists"""

    def test_login_required_for_manufacturers(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_cars(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_for_drivers(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateSearchAndValidationTests(TestCase):
    """Test search features and custom validation for authenticated users"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="AAA12345"
        )
        self.client.login(username="testuser", password="password123")

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford", country="USA"
        )

        self.car1 = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Mustang", manufacturer=self.manufacturer2
        )

        self.driver1 = get_user_model().objects.create_user(
            username="driver_bob",
            password="password123",
            license_number="BBB11111"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver_alice",
            password="password123",
            license_number="CCC22222"
        )

    def test_search_manufacturer_by_name(self):
        res = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "toy"}
        )
        self.assertIn(self.manufacturer1, res.context["manufacturer_list"])
        self.assertNotIn(self.manufacturer2, res.context["manufacturer_list"])

    def test_search_car_by_model(self):
        res = self.client.get(reverse("taxi:car-list"), {"model": "must"})
        self.assertIn(self.car2, res.context["car_list"])
        self.assertNotIn(self.car1, res.context["car_list"])

    def test_search_driver_by_username(self):
        res = self.client.get(
            reverse("taxi:driver-list"), {"username": "alice"}
        )
        self.assertIn(self.driver2, res.context["driver_list"])
        self.assertNotIn(self.driver1, res.context["driver_list"])

    def test_valid_license_number_passes(self):
        from taxi.forms import validate_license_number
        from django.core.exceptions import ValidationError

        try:
            validate_license_number("XYZ98765")
        except ValidationError:
            msg = (
                "validate_license_number raised "
                "ValidationError unexpectedly!"
            )
            self.fail(msg)

    def test_invalid_license_length_fails(self):
        from taxi.forms import validate_license_number
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            validate_license_number("XYZ9876")

    def test_invalid_license_letters_fails(self):
        from taxi.forms import validate_license_number
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            validate_license_number("xyZ98765")

    def test_invalid_license_digits_fails(self):
        from taxi.forms import validate_license_number
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            validate_license_number("XYZ9876A")
