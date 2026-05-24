from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number
from taxi.models import Manufacturer, Car


class SearchFeaturesTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testdriver",
            password="password123",
            license_number="ABC12345",
        )
        self.other_driver = get_user_model().objects.create_user(
            username="johndoe",
            password="password123",
            license_number="XYZ54321",
        )
        self.client.login(username="testdriver", password="password123")

        self.man_toyota = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.man_tesla = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )

        self.car_camry = Car.objects.create(
            model="Camry", manufacturer=self.man_toyota
        )
        self.car_model_s = Car.objects.create(
            model="Model S", manufacturer=self.man_tesla
        )

    def test_search_manufacturer_by_name(self):
        url = reverse("taxi:manufacturer-list")

        response = self.client.get(url, {"name": "toy"})

        self.assertIn(self.man_toyota, response.context["manufacturer_list"])
        self.assertNotIn(self.man_tesla, response.context["manufacturer_list"])

    def test_search_car_by_model(self):
        url = reverse("taxi:car-list")

        response = self.client.get(url, {"model": "Model"})

        self.assertIn(self.car_model_s, response.context["car_list"])
        self.assertNotIn(self.car_camry, response.context["car_list"])

    def test_search_driver_by_username(self):
        url = reverse("taxi:driver-list")

        response = self.client.get(url, {"username": "john"})

        self.assertIn(self.other_driver, response.context["driver_list"])
        self.assertNotIn(self.user, response.context["driver_list"])


class CustomCoreFeaturesTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="main_driver",
            password="password123",
            license_number="AAA11111",
        )
        self.client.login(username="main_driver", password="password123")

        self.manufacturer = Manufacturer.objects.create(
            name="Ford", country="USA"
        )
        self.car = Car.objects.create(
            model="Mustang", manufacturer=self.manufacturer
        )

    def test_license_number_valid(self):
        valid_license = "ABC12345"
        self.assertEqual(validate_license_number(valid_license), valid_license)

    def test_license_number_wrong_length(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("AB12345")
        self.assertIn(
            "License number should consist of 8 characters",
            context.exception.message,
        )

    def test_license_number_first_3_not_uppercase_letters(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("abC12345")
        self.assertIn(
            "First 3 characters should be uppercase letters",
            context.exception.message,
        )

        with self.assertRaises(ValidationError) as context:
            validate_license_number("AB112345")
        self.assertIn(
            "First 3 characters should be uppercase letters",
            context.exception.message,
        )

    def test_license_number_last_5_not_digits(self):
        with self.assertRaises(ValidationError) as context:
            validate_license_number("ABC1234A")
        self.assertIn(
            "Last 5 characters should be digits", context.exception.message
        )

    def test_toggle_assign_to_car_adds_driver(self):
        self.assertNotIn(self.car, self.user.cars.all())

        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        response = self.client.get(url)

        self.assertRedirects(
            response, reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )
        self.assertIn(self.car, self.user.cars.all())

    def test_toggle_assign_to_car_removes_driver(self):
        self.user.cars.add(self.car)
        self.assertIn(self.car, self.user.cars.all())

        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        response = self.client.get(url)

        self.assertRedirects(
            response, reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )
        self.assertNotIn(self.car, self.user.cars.all())
