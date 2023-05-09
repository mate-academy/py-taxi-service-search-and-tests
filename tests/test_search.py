from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class SearchFormTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            license_number="QWE12345",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(MANUFACTURER_LIST_URL + "?name=Ford")

        self.assertEqual(
            list(response.context["manufacturer-list"]),
            list(Manufacturer.objects.filter(name__icontains="Ford"))
        )

    def test_search_car_by_model(self):
        response = self.client.get(CAR_LIST_URL + "?model=Focus")

        self.assertEqual(
            list(response.context["car-list"]),
            list(Car.objects.filter(name__icontains="Focus"))
        )

    def test_search_driver_by_username(self):
        response = self.client.get(DRIVER_LIST_URL + "?Username=admin")

        self.assertEqual(
            list(response.context["driver-list"]),
            list(Car.objects.filter(name__icontains="admin"))
        )
