from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PrivateManufacturerListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Testuser",
            password="Test12345"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test1")
        Manufacturer.objects.create(name="Test2")

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_search_manufacturer(self):
        Manufacturer.objects.create(
            name="Daimler",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="BMW"
        )
        response = self.client.get(MANUFACTURERS_URL, {"name": "Audi"})
        search_manufacturer = Manufacturer.objects.filter(name="Audi")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(search_manufacturer)
        )


class PublicManufacturerListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)
