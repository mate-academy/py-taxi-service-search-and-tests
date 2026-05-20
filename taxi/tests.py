from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number
from taxi.models import Car, Driver, Manufacturer


class PublicPageTests(TestCase):
    def test_login_required_for_index(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertNotEqual(response.status_code, 200)


class TaxiServiceTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john",
            password="test12345",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_index_shows_counts_and_increases_visits(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Car.objects.create(model="Camry", manufacturer=manufacturer)

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)

    def test_license_number_validation(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

        with self.assertRaises(ValidationError):
            validate_license_number("AB12345")

        with self.assertRaises(ValidationError):
            validate_license_number("ABC12DDD")


class SearchTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john_driver",
            password="test12345",
            license_number="ABC12345",
        )
        Driver.objects.create_user(
            username="alex_driver",
            password="test12345",
            license_number="DEF12345",
        )

        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        honda = Manufacturer.objects.create(name="Honda", country="Japan")

        Car.objects.create(model="Camry", manufacturer=toyota)
        Car.objects.create(model="Civic", manufacturer=honda)

        self.client.force_login(self.driver)

    def test_search_manufacturers_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"manufacturer_name": "toy"},
        )

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")

    def test_search_cars_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"car_model": "cam"},
        )

        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Civic")

    def test_search_drivers_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"driver_username": "john"},
        )

        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "alex_driver")
