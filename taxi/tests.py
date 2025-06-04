from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(username="user", password="testpass123")
        self.client.login(username="user", password="testpass123")

        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Tesla")
        Manufacturer.objects.create(name="BMW")

    def test_search_manufacturers_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list") + "?name=Tes")
        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(manufacturers.count(), 1)
        self.assertEqual(manufacturers[0].name, "Tesla")

# Create your tests here.
