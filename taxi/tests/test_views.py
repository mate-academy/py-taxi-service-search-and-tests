from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Car, Manufacturer

DETAIL_URL_NAMES = [
    "manufacturer-update",
    "car-detail",
    "car-update",
    "car-delete",
    "driver-detail",
    "driver-update",
]

GROUP_URL_NAMES = [
    "index",
    "manufacturer-list",
    "manufacturer-create",
    "car-list",
    "car-create",
    "driver-list",
    "driver-create"
]

APP_NAME = "taxi"


class PublicViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_group_view_login_required(self):
        for url_name in GROUP_URL_NAMES:
            url = reverse(f"{APP_NAME}:{url_name}")
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)

    def test_detail_view_login_required(self):
        for url_name in DETAIL_URL_NAMES:
            url = reverse(f"{APP_NAME}:{url_name}", args=[1, ])
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="FirstUserName",
            first_name="FirstName",
            last_name="LastName",
            email="Email@Address",
            license_number="ADM12345",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer", country="Country"
        )
        Car.objects.create(model="Model1", manufacturer=self.manufacturer)
        Car.objects.create(model="Model2", manufacturer=self.manufacturer)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_manufacturer_search_form(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Honda", country="Japan")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search_query": "Ford"}
        )

        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertIn("Ford", str(response.content))
        self.assertNotIn(
            "Honda",
            str(response.content)
        )

    def test_cars_search_form(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"search_query": "Model1"}
        )
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertIn("Model1", str(response.content))
        self.assertNotIn("Model2", str(response.content))

    def test_drivers_search_form(self):
        get_user_model().objects.create_user(
            username="AnotherUserName",
            first_name="SomeName",
            last_name="LastName",
            email="Email@Adress",
            license_number="ADM12346",
            password="<PASSWORD>",
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search_query": "another"})

        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(response.context["driver_list"][0].username, "AnotherUserName")
