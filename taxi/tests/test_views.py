from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class TestIndex(TestCase):
    INDEX_URL = reverse("taxi:index")

    def test_login(self):
        response = self.client.get(self.INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class TestDiverListPagination(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user", password="1qazcde3")
        self.client.login(username="admin.user", password="1qazcde3")

        for i in range(5):
            Driver.objects.create_user(
                username=f"user{i}",
                password=f"1qazcde{i}",
                license_number=f"ABC{i}1234"
            )

    def test_driver_pagination(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

        self.assertEqual(len(response.context["driver_list"]), 5)

        response_page_2 = self.client.get(reverse(
            "taxi:driver-list") + "?page=2")
        self.assertEqual(len(response_page_2.context["driver_list"]), 1)


class TestQueryset(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin.user", password="1qazcde3"
        )
        self.client.login(username="admin.user", password="1qazcde3")
        self.manufacturer = Manufacturer.objects.create(
            name="CAR"
            , country="Germany")
        Car.objects.create(model="BMW", manufacturer=self.manufacturer)
        Car.objects.create(model="Mercedes", manufacturer=self.manufacturer)

    def test_get_queryset(self):
        url = reverse("taxi:car-list") + "?title=bmw"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["car_list"][0].model, "BMW")
