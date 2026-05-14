from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.forms import validate_license_number
from taxi.models import Manufacturer, Car


User = get_user_model()


class LicenseNumberValidationTests(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_number_length_invalid(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")

    def test_license_number_first_three_chars_invalid(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_license_number_last_five_chars_invalid(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC12abc")


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.assertEqual(str(manufacturer), "BMW Germany")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        car = Car.objects.create(
            model="A6",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), "A6")

    def test_driver_str(self):
        driver = User.objects.create_user(
            username="driver1",
            password="test12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )

        self.assertEqual(str(driver), "driver1 (John Doe)")

    def test_driver_get_absolute_url(self):
        driver = User.objects.create_user(
            username="driver2",
            password="test12345",
            license_number="BCD12345",
        )

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )


class PublicViewsTests(TestCase):
    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)


class SearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="test12345",
            license_number="AAA12345",
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"},
        )

        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )

        Car.objects.create(model="Model S", manufacturer=manufacturer)
        Car.objects.create(model="Cybertruck", manufacturer=manufacturer)

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Model"},
        )

        self.assertContains(response, "Model S")
        self.assertNotContains(response, "Cybertruck")

    def test_search_driver_by_username(self):
        User.objects.create_user(
            username="john_driver",
            password="test12345",
            license_number="BBB12345",
        )
        User.objects.create_user(
            username="mike_driver",
            password="test12345",
            license_number="CCC12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )

        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "mike_driver")
