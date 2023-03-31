from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="pass12345word",
        )

        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Test", country="Test")
        Manufacturer.objects.create(name="Qwerty", country="Country")

    def test_retrieve_manufacturer(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        res = self.client.get(MANUFACTURER_LIST_URL + "?name=e")

        manufacturers = Manufacturer.objects.filter(name__icontains="e")
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "First",
            "country": "Second"
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])
        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])
