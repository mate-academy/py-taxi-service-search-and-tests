from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number
from taxi.models import Car, Manufacturer


class SearchViewTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="taxi.driver",
            password="test-password",
            license_number="TAX12345",
        )
        self.other_driver = get_user_model().objects.create_user(
            username="road.runner",
            password="test-password",
            license_number="RUN12345",
        )
        self.tesla = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        self.ford = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )
        self.model_s = Car.objects.create(
            model="Model S",
            manufacturer=self.tesla,
        )
        self.fiesta = Car.objects.create(
            model="Fiesta",
            manufacturer=self.ford,
        )
        self.client.force_login(self.driver)

    def test_search_drivers_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "RUN"},
        )

        self.assertEqual(
            list(response.context["driver_list"]),
            [self.other_driver],
        )

    def test_search_cars_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "model"},
        )

        self.assertEqual(list(response.context["car_list"]), [self.model_s])

    def test_search_manufacturers_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "tes"},
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [self.tesla],
        )

    def test_empty_search_returns_all_cars(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": ""},
        )

        self.assertEqual(
            list(response.context["car_list"]),
            [self.model_s, self.fiesta],
        )


class ModelTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="taxi.driver",
            first_name="Taxi",
            last_name="Driver",
            license_number="TAX12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer,
        )

    def test_manufacturer_string_representation(self):
        self.assertEqual(str(self.manufacturer), "Tesla USA")

    def test_driver_string_representation(self):
        self.assertEqual(str(self.driver), "taxi.driver (Taxi Driver)")

    def test_car_string_representation(self):
        self.assertEqual(str(self.car), "Model S")

    def test_driver_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
        )


class DriverLicenseValidationTests(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("TAX12345"), "TAX12345")

    def test_license_number_must_have_eight_characters(self):
        with self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters",
        ):
            validate_license_number("TAX1234")

    def test_license_number_must_start_with_uppercase_letters(self):
        with self.assertRaisesMessage(
            ValidationError,
            "First 3 characters should be uppercase letters",
        ):
            validate_license_number("tax12345")

    def test_license_number_must_end_with_digits(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Last 5 characters should be digits",
        ):
            validate_license_number("TAX12ABC")


class CoreFeatureTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="taxi.driver",
            password="test-password",
            license_number="TAX12345",
        )
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=manufacturer,
        )
        self.client.force_login(self.driver)

    def test_home_page_visit_counter(self):
        first_response = self.client.get(reverse("taxi:index"))
        second_response = self.client.get(reverse("taxi:index"))

        self.assertEqual(first_response.context["num_visits"], 1)
        self.assertEqual(second_response.context["num_visits"], 2)

    def test_driver_can_toggle_car_assignment(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.pk])

        self.client.get(url)
        self.assertTrue(self.driver.cars.filter(pk=self.car.pk).exists())

        self.client.get(url)
        self.assertFalse(self.driver.cars.filter(pk=self.car.pk).exists())

    def test_car_create_page_is_rendered(self):
        response = self.client.get(reverse("taxi:car-create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_driver_can_be_deleted(self):
        driver_to_delete = get_user_model().objects.create_user(
            username="retired.driver",
            license_number="RET12345",
        )

        response = self.client.post(
            reverse("taxi:driver-delete", args=[driver_to_delete.pk]),
        )

        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertFalse(
            get_user_model().objects.filter(pk=driver_to_delete.pk).exists()
        )
