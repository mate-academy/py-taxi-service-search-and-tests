from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class TestSearchFrom(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "test123"
        )
        self.client.force_login(self.user)

    def test_search_from_manufacturer(self) -> None:
        Manufacturer.objects.create(
            name="test",
            country="Country"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name="test"))
        )

    def test_search_from_driver(self) -> None:
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "test"}
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(username="test"))
        )

    def test_search_from_car(self) -> None:
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(
                country="test", name="test"
            )
        )

        response = self.client.get(
            reverse("taxi:car-list"), {"model": "test_model"}
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["car_list"]),
            list(Car.objects.filter(model="test_model"))
        )
