from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="test12345",
            license_number="ADM12345",
        )
        self.client.force_login(self.user)

    def test_manufacturer_search_by_name_is_case_insensitive(self):
        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        tesla = Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "T"},
        )

        self.assertCountEqual(
            response.context["manufacturer_list"],
            [toyota, tesla],
        )

    def test_manufacturer_empty_search_returns_all(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": ""},
        )

        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_manufacturer_search_without_results(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "xyz"},
        )

        self.assertEqual(len(response.context["manufacturer_list"]), 0)

    def test_car_search_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        corolla = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer,
        )
        Car.objects.create(model="Camry", manufacturer=manufacturer)

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "co"},
        )

        self.assertCountEqual(response.context["car_list"], [corolla])

    def test_driver_search_by_username(self):
        driver_model = get_user_model()
        john = driver_model.objects.create_user(
            username="john.smith",
            password="test12345",
            license_number="JOH12345",
        )
        jane = driver_model.objects.create_user(
            username="jane.doe",
            password="test12345",
            license_number="JAN12345",
        )
        driver_model.objects.create_user(
            username="bob.brown",
            password="test12345",
            license_number="BOB12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "j"},
        )

        self.assertCountEqual(response.context["driver_list"], [john, jane])

    def test_search_form_keeps_entered_value(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"},
        )

        self.assertEqual(
            response.context["search_form"].initial["name"],
            "toy",
        )

    def test_pagination_keeps_search_query(self):
        for number in range(1, 7):
            Manufacturer.objects.create(
                name=f"Brand {number}",
                country="Country",
            )
        Manufacturer.objects.create(name="Toyota", country="Japan")
        url = reverse("taxi:manufacturer-list")

        first_page = self.client.get(url, {"name": "brand"})
        second_page = self.client.get(url, {"name": "brand", "page": 2})

        self.assertEqual(len(first_page.context["manufacturer_list"]), 5)
        self.assertEqual(len(second_page.context["manufacturer_list"]), 1)
        self.assertContains(first_page, "name=brand&amp;page=2")
