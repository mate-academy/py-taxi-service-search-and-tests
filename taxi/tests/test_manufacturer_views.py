from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.create_manufacturers()

    def create_manufacturers(self):
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota",
                                                         country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(name="Honda",
                                                         country="Japan")
        self.manufacturer3 = Manufacturer.objects.create(name="Ford",
                                                         country="USA")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        for manufacturer in manufacturers:
            self.assertContains(response, manufacturer.name)

    def test_search_manufacturers(self):
        search_term = "Toyota"
        response = self.client.get(MANUFACTURER_URL, {"name": search_term})
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.filter(
            name__icontains=search_term
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        for manufacturer in manufacturers:
            self.assertContains(response, manufacturer.name)
