from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicViewTests(TestCase):
    def test_login_required(self):
        """Test that login is required to access the index page"""
        res = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(res.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )

    def test_retrieve_manufacturers(self):
        """Test retrieving manufacturer list"""
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Tesla")

    def test_retrieve_cars(self):
        """Test retrieving car list"""
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Model S")


class SearchTests(TestCase):
    def setUp(self):
        # Tworzymy kierowców z unikalnymi numerami licencji
        self.user = get_user_model().objects.create_user(
            username="driver1",
            password="password123",
            license_number="ABC11111"
        )
        get_user_model().objects.create_user(
            username="driver2",
            password="password123",
            license_number="XYZ99999"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(name="Audi")
        self.manufacturer2 = Manufacturer.objects.create(name="BMW")

        # Dodajemy ordering do aut, aby uniknąć UnorderedObjectListWarning
        self.car1 = Car.objects.create(
            model="A6",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="M5",
            manufacturer=self.manufacturer2
        )

    def test_search_manufacturer_by_name(self):
        """Test searching for manufacturer by name"""
        res = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Audi"}
        )
        self.assertContains(res, "Audi")
        self.assertNotContains(res, "BMW")

    def test_search_car_by_model(self):
        """Test searching for car by model"""
        res = self.client.get(
            reverse("taxi:car-list"),
            {"model": "A6"}
        )
        self.assertContains(res, "A6")
        self.assertNotContains(res, "M5")

    def test_search_driver_by_username(self):
        """Test searching for driver by username"""
        res = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver1"}
        )
        self.assertContains(res, "driver1")
        self.assertNotContains(res, "driver2")


class FormTests(TestCase):
    def test_validate_license_number(self):
        """Test that license number validation works correctly"""
        from taxi.forms import validate_license_number
        from django.core.exceptions import ValidationError

        # Valid license
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

        # Invalid: too short
        with self.assertRaises(ValidationError):
            validate_license_number("AB12345")

        # Invalid: first 3 not uppercase letters
        with self.assertRaises(ValidationError):
            validate_license_number("abC12345")

        # Invalid: last 5 not digits
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234a")
