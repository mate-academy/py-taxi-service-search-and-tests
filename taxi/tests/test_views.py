from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="123test",
        )
        self.client.force_login(self.user)

    def test_retrive_manufacturer(self):
        Manufacturer.objects.create(name="test", country="test")
        Manufacturer.objects.create(name="test2", country="test2")
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_manufacturer_update(self):
        self.manufacturer = Manufacturer.objects.create(name="test",
                                                        country="test")
        url = reverse("taxi:manufacturer-update",
                      args=[self.manufacturer.id])
        new_data = {
            "name": "test2",
            "country": "test2",
        }
        res = self.client.post(url, new_data)
        self.assertEqual(res.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, new_data["name"])

    def test_manufacturer_create(self):
        url = reverse("taxi:manufacturer-create")
        new_data = {
            "name": "test",
            "country": "test",
        }
        self.client.post(url, new_data)
        new_manufacturer = Manufacturer.objects.get(name=new_data["name"])
        self.assertEqual(new_manufacturer.name, new_data["name"])
