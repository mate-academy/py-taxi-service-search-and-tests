from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number
from taxi.models import Car, Manufacturer


class TaxiServiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create_user(
            username="search.driver",
            password="test-password",
            license_number="SRC12345",
        )
        cls.other_driver = get_user_model().objects.create_user(
            username="another.user",
            password="test-password",
            license_number="OTH12345",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Search Motors",
            country="Ukraine",
        )
        cls.other_manufacturer = Manufacturer.objects.create(
            name="Different Factory",
            country="Poland",
        )
        cls.car = Car.objects.create(
            model="Search Car",
            manufacturer=cls.manufacturer,
        )
        cls.other_car = Car.objects.create(
            model="Different Vehicle",
            manufacturer=cls.other_manufacturer,
        )

    def setUp(self):
        self.client.force_login(self.driver)


class SearchViewTests(TaxiServiceTestCase):
    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "SEARCH"},
        )

        self.assertEqual(list(response.context["driver_list"]), [self.driver])
        self.assertEqual(
            response.context["search_form"]["username"].value(),
            "SEARCH",
        )

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "search"},
        )

        self.assertEqual(list(response.context["car_list"]), [self.car])

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "motors"},
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [self.manufacturer],
        )

    def test_empty_search_returns_all_objects(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})

        self.assertEqual(response.context["paginator"].count, 2)


class CoreFeatureTests(TaxiServiceTestCase):
    def test_list_views_require_login(self):
        self.client.logout()

        response = self.client.get(reverse("taxi:driver-list"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('taxi:driver-list')}",
        )

    def test_toggle_assigns_and_removes_current_driver(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.pk])

        self.client.get(url)
        self.assertTrue(self.car.drivers.filter(pk=self.driver.pk).exists())

        self.client.get(url)
        self.assertFalse(self.car.drivers.filter(pk=self.driver.pk).exists())

    def test_license_number_validation(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

        invalid_numbers = ("abc12345", "AB123456", "ABCD1234")
        for license_number in invalid_numbers:
            with self.subTest(license_number=license_number):
                with self.assertRaises(ValidationError):
                    validate_license_number(license_number)

    def test_model_string_representations(self):
        self.assertEqual(str(self.car), "Search Car")
        self.assertEqual(str(self.manufacturer), "Search Motors Ukraine")
