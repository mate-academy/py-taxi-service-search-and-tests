from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test_user",
            email="myemail@gmail.com",
            password="password123",
            license_number="DSV89273"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Mazda"
        )

        self.car1 = Car.objects.create(
            model="MX5",
            manufacturer=self.manufacturer,
        )

        self.car2 = Car.objects.create(
            model="RX7",
            manufacturer=self.manufacturer,
        )

        self.car1.drivers.add(self.user)
        self.car2.drivers.add(self.user)

    def test_car(self):
        self.client.force_login(self.user)

        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "MX"})

        self.assertContains(response, "MX5")
        self.assertNotContains(response, "RX7")

        self.assertEqual(response.status_code, 200)

    def test_search_car_all(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("taxi:car-list"), {"model": ""})

        self.assertContains(response, "MX5")
        self.assertContains(response, "RX7")

    def test_search_no_results_car(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "NonExistent"}
        )

        self.assertEqual(len(response.context["car_list"]), 0)
