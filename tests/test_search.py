from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from taxi.models import Car, Manufacturer


class SearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )

    def test_check_search_car(self):
        self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Continental",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        test_car_model = "Continental"
        url = reverse("taxi:car-list")
        query_kwargs = {"model": test_car_model}
        response = self.client.get(
            f"{url}?{urlencode(query_kwargs)}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['car_list']), 1)

    def test_check_search_no_car(self):
        self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Continental",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        test_car_model = "Bentley"
        url = reverse("taxi:car-list")
        query_kwargs = {"model": test_car_model}
        response = self.client.get(
            f"{url}?{urlencode(query_kwargs)}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['car_list']), 0)

    def test_check_search_driver(self):
        test_driver_username = "admin.user"
        url = reverse("taxi:driver-list")
        query_kwargs = {"username": test_driver_username}
        response = self.client.get(
            f"{url}?{urlencode(query_kwargs)}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['driver_list']), 1)

    def test_check_search_no_driver(self):
        test_driver_username = "dexter"
        url = reverse("taxi:driver-list")
        query_kwargs = {"username": test_driver_username}
        response = self.client.get(
            f"{url}?{urlencode(query_kwargs)}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['driver_list']), 0)

    def test_check_search_manufacturer(self):
        test_manufacturer_name = "lincoln"
        url = reverse("taxi:manufacturer-list")
        query_kwargs = {"name": test_manufacturer_name}
        response = self.client.get(
            f"{url}?{urlencode(query_kwargs)}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['manufacturer_list']), 1)

    def test_check_search_no_manufacturer(self):
        test_manufacturer_name = "renault"
        url = reverse("taxi:manufacturer-list")
        query_kwargs = {"name": test_manufacturer_name}
        response = self.client.get(
            f"{url}?{urlencode(query_kwargs)}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['manufacturer_list']), 0)
