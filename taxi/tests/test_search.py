from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class AuthenticatedSearchTestMixin:
    def setUp(self):
        self.logged_in_driver = Driver.objects.create_user(
            username="searcher",
            password="Strong-password-123",
            license_number="ABC12345",
        )
        self.client.force_login(self.logged_in_driver)


class ManufacturerSearchTests(AuthenticatedSearchTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        Manufacturer.objects.create(name="Ford Motor", country="USA")
        Manufacturer.objects.create(name="Volvo", country="Sweden")

    def test_search_filters_by_case_insensitive_name_and_keeps_query(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "fOrD"},
        )

        self.assertEqual(
            [
                manufacturer.name
                for manufacturer in response.context["manufacturer_list"]
            ],
            ["Ford Motor"],
        )
        self.assertEqual(
            response.context["search_form"]["name"].value(), "fOrD"
        )

    def test_empty_search_returns_all_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(len(response.context["manufacturer_list"]), 2)


class CarSearchTests(AuthenticatedSearchTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        manufacturer = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        Car.objects.create(model="Honda Civic", manufacturer=manufacturer)
        Car.objects.create(model="Honda Accord", manufacturer=manufacturer)

    def test_search_filters_by_case_insensitive_model_and_keeps_query(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"name": "cIvIc"}
        )

        self.assertEqual(
            [car.model for car in response.context["car_list"]],
            ["Honda Civic"],
        )
        self.assertEqual(
            response.context["search_form"]["name"].value(), "cIvIc"
        )

    def test_empty_search_returns_all_cars(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(len(response.context["car_list"]), 2)


class DriverSearchTests(AuthenticatedSearchTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        Driver.objects.create_user(
            username="JaneDriver",
            password="Strong-password-123",
            license_number="DEF12345",
        )
        Driver.objects.create_user(
            username="AlexDriver",
            password="Strong-password-123",
            license_number="GHI12345",
        )

    def test_search_filters_by_case_insensitive_username_and_keeps_query(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"name": "jAnE"}
        )

        self.assertEqual(
            [driver.username for driver in response.context["driver_list"]],
            ["JaneDriver"],
        )
        self.assertEqual(
            response.context["search_form"]["name"].value(), "jAnE"
        )

    def test_empty_search_returns_all_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(len(response.context["driver_list"]), 3)
