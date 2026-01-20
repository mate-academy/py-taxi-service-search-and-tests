from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="toyota test",
            country="Japan test"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="toyota test2", country="Japan test2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_create_manufacturer(self):
        form_data = {
            "name": "toyota test1",
            "country": "Japan test1",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])
        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_update_manufacturer(self):
        update_url = reverse(
            "taxi:manufacturer-update",
            args=[self.manufacturer.id]
        )
        updated_data = {"name": "Honda", "country": "Japan"}
        response = self.client.post(update_url, data=updated_data)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, updated_data["name"])
        self.assertEqual(self.manufacturer.country, updated_data["country"])

    def test_delete_manufacturer(self):
        delete_url = reverse(
            "taxi:manufacturer-delete",
            args=[self.manufacturer.id]
        )
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )
