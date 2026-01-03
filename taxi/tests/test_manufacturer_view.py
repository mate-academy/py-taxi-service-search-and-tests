from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):

    def test_login_requires(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test Manufacturer1")
        Manufacturer.objects.create(name="Test Manufacturer2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "New Manufacturer",
            "country": "New Country"
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        self.assertTrue(
            Manufacturer.objects.filter(
                name=form_data["name"],
                country=form_data["country"]
            ).exists()
        )
