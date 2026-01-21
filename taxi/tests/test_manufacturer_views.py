from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):

    def test_login_required(self):
        test_response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(test_response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="mypass321"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="first", country="nocountry")
        Manufacturer.objects.create(name="second", country="best")
        test_response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(test_response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(test_response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(test_response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        response = self.client.get(MANUFACTURER_URL, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(manufacturer1, response.context["manufacturer_list"])

        response = self.client.get(MANUFACTURER_URL, {"name": "Toy"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(manufacturer1, response.context["manufacturer_list"])

        response = self.client.get(MANUFACTURER_URL, {"name": "Ford"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(manufacturer1, response.context["manufacturer_list"])
