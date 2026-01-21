from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="Test", country="Test")
        delete_url = reverse(
            "taxi:manufacturer-delete", args=[manufacturer.id]
        )
        response = self.client.post(delete_url)
        self.assertFalse(
            Manufacturer.objects.filter(id=manufacturer.id).exists()
        )
        success_url = reverse("taxi:manufacturer-list")
        self.assertRedirects(response, success_url)


CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/car_list.html")
