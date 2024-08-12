from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 302)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="FDIFI44434",
        )
        self.client.force_login(self.user)

    def test_authorised_user_can_access(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturers(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Manufacturer",
            country="test"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Manufacturer2",
            country="test"
        )
        response = self.client.get(MANUFACTURER_URL)
        queryset = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(queryset)
        )
        self.assertContains(response, manufacturer1.name)
        self.assertContains(response, manufacturer2.name)
