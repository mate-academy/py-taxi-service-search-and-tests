from django.test import TestCase

from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerLoginTest(TestCase):
    def test_login(self):
        get_result = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(get_result.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="qwerfghnm"
        )
        self.client.force_login(self.user)

    def test_login(self):
        get_result = self.client.get(MANUFACTURER_URL)
        self.assertEqual(get_result.status_code, 200)

    def test_context_view(self):
        Manufacturer.objects.create(name="test_1")
        Manufacturer.objects.create(name="test_2")
        get_result = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(get_result.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_filter_view(self):
        Manufacturer.objects.create(name="first")
        Manufacturer.objects.create(name="second")
        get_result = self.client.get(MANUFACTURER_URL, {"name": "st"})
        manufacturers_filtered = Manufacturer.objects.filter(
            name__icontains="st"
        )
        self.assertEqual(
            list(get_result.context["manufacturer_list"]),
            list(manufacturers_filtered)
        )
