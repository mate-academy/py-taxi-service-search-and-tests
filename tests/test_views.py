from unittest import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Manufacturer


class ManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_user",
            password="87ASDHADIK7asd7IA6SD",
            first_name="Mike",
            last_name="Smith",
            license_number="ABB1111",
        )
        self.url_create = reverse("taxi:manufacturer-create")
        self.url_list = reverse("taxi:manufacturer-list")
        self.client = Client()
        self.client.force_login(self.user)

    def tearDown(self):
        self.user.delete()

    def test_create_manufacturer(self):
        manufacturer_data = {
            "name": "ZAZ",
            "country": "Ukraine",
        }
        response = self.client.post(self.url_create, data=manufacturer_data)
        created_manufacturer = Manufacturer.objects.filter(name="ZAZ").exists()
        self.assertTrue(created_manufacturer)
        self.assertEqual(response.url, reverse("taxi:manufacturer-list"))

    def test_create_manufacturer_invalid_data(self):
        manufacturer_data = {
            "name": "",
            "country": "TestCountry",
        }
        response = self.client.post(self.url_create, data=manufacturer_data)
        form = response.context.get("form")
        self.assertTrue(form.errors)

        created_manufacturer = Manufacturer.objects.filter(
            country="TestCountry"
        ).exists()
        self.assertFalse(created_manufacturer)

    def test_create_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url_list)
        self.assertIn(reverse("login"), response.url)
