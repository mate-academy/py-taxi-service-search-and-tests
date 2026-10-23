from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="testuser6", country="Germany")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser7",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_by_manufacturer(self):
        Manufacturer.objects.create(name="Bugatti", country="France")
        Manufacturer.objects.create(name="Volvo", country="Sweden")
        response = self.client.get(
            reverse("taxi:manufacturer-list")
            + "?name=Bugatti"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bugatti")
        self.assertNotContains(response, "Volvo")
