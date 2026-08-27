from django.urls import reverse
from taxi.models import Manufacturer
from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class PublicManufacturerTest(TestCase):
    MANUFACTURER_URL = reverse("taxi:manufacturer-list")

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(self.MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    MANUFACTURER_URL = reverse("taxi:manufacturer-list")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="bogdanchik",
            password="bbb1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )
        Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )
        response = self.client.get(self.MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            response.context["manufacturer_list"],
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_search_manufacturer(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        response = self.client.get(self.MANUFACTURER_URL, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
