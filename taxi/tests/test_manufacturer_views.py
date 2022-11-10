from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturersTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturersTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="test123user"
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Manufname1",
            country="Manufcountry1"
        )
        Manufacturer.objects.create(
            name="Manufname2",
            country="Manufcountry2"
        )

        manufacturers = Manufacturer.objects.all()

        response = self.client.get(MANUFACTURERS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
