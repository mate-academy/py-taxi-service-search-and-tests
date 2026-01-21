from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create(self):
        res = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_update(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        res = self.client.get(
            reverse("taxi:manufacturer-update",
                    args=[manufacturer.id]
                    )
        )
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "New Manufacturer",
            "country": "New Country",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])
