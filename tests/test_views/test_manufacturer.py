from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class TestLoginRequired(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test", password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="testformat2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, manufacturer.name)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
