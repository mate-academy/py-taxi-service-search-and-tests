from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Old Name", country="Old Country"
        )

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {"name": "Ford", "country": "USA"}
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Ford").exists())

    def test_update_manufacturer_view(self):
        form_data = {"name": "Updated Name", "country": "Updated Country"}
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            data=form_data,
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Updated Name")
        self.assertEqual(self.manufacturer.country, "Updated Country")

    def test_delete_manufacturer(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )
