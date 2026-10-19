from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import SearchForm
from taxi.models import Car, Manufacturer


class SearchFormTests(TestCase):
    def test_search_form_valid_with_empty_query(self):
        form = SearchForm(data={"query": ""})

        self.assertTrue(form.is_valid())

    def test_search_form_valid_with_query(self):
        form = SearchForm(data={"query": "abc"})

        self.assertTrue(form.is_valid())


class SearchFeatureTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            password="test12345",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        self.manufacturer_toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.manufacturer_bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.car_camry = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer_toyota,
        )
        self.car_x5 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer_bmw,
        )

        self.driver_john = get_user_model().objects.create_user(
            username="john",
            password="test12345",
            license_number="AAA11111",
        )
        self.driver_mike = get_user_model().objects.create_user(
            username="mike",
            password="test12345",
            license_number="BBB22222",
        )

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "john")
        self.assertNotContains(response, "mike")

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "Camry"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "X5")

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": "Toyota"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")


class CoreFeatureTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test12345",
            license_number="ABC12345",
        )

    def test_index_page_requires_login(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertNotEqual(response.status_code, 200)

    def test_index_page_available_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )
        car = Car.objects.create(
            model="A4",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), "A4")
