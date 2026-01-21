from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer


class FormTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="admin_user",
            password="securepass123"
        )
        self.client.force_login(self.admin)

        self.manufacturer = Manufacturer.objects.create(name="AltroMotors")

    def test_valid_driver_license_number(self):
        """Check that form with valid license number is valid."""
        form_data = {"license_number": "XYZ67890"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_driver_license_number(self):
        """Check that car search filters car models correctly."""
        form_data = {"license_number": "XY678901"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_search_filters_models_correctly(self):
        """Check that car search filters car models correctly."""
        models = ["Corsa", "Phantom", "RZ5", "Falcon"]
        for model in models:
            Car.objects.create(model=model, manufacturer=self.manufacturer)

        response = self.client.get(reverse("taxi:car-list") + "?model=a")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 4)

    def test_driver_search_returns_expected_user(self):
        """Check that driver search returns only matching usernames."""
        drivers = [
            {"username": "viktor",
             "password": "pass123",
             "license_number": "RTY45678"},
            {"username": "denis",
             "password": "pass123",
             "license_number": "QWE98765"},
            {"username": "artemio",
             "password": "pass123",
             "license_number": "BVC65432"},
            {"username": "ghost_man",
             "password": "pass123",
             "license_number": "LMN32109"},
        ]

        for driver in drivers:
            get_user_model().objects.create_user(**driver)

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=art")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_manufacturer_search_finds_all_matches(self):
        """Check that manufacturer search returns matching names."""
        manufacturers = [
            {"name": "GenX", "country": "Germany"},
            {"name": "Argenta", "country": "Italy"},
            {"name": "Megatek", "country": "Japan"},
            {"name": "GigaDrive", "country": "USA"},
        ]

        for data in manufacturers:
            Manufacturer.objects.create(**data)

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=g")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
