from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class TaxiSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver1 = Driver.objects.create_user(
            username="john_driver",
            password="testpass123",
            license_number="ABC12345",
        )
        cls.driver2 = Driver.objects.create_user(
            username="mary_driver",
            password="testpass123",
            license_number="XYZ12345",
        )

        cls.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        cls.manufacturer2 = Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )

        cls.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=cls.manufacturer1,
        )
        cls.car2 = Car.objects.create(
            model="Civic",
            manufacturer=cls.manufacturer2,
        )

    def setUp(self):
        self.client.force_login(self.driver1)

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            [self.driver1],
        )

    def test_driver_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "JOHN"},
        )

        self.assertContains(response, "john_driver")
        self.assertNotContains(response, "mary_driver")

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "cor"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            [self.car1],
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [self.manufacturer1],
        )

    def test_empty_search_shows_all_records(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["driver_list"].count(),
            2,
        )

    def test_driver_detail_page_is_accessible(self):
        response = self.client.get(
            reverse(
                "taxi:driver-detail",
                kwargs={"pk": self.driver1.pk},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_manufacturer_string_representation(self):
        self.assertEqual(str(self.manufacturer1), "Toyota Japan")

    def test_car_string_representation(self):
        self.assertEqual(str(self.car1), "Corolla")
