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
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Tesla", country="USA")
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_get_queryset_with_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=BMW"
        )
        manufacturer_list = response.context["manufacturer_list"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(manufacturer_list), 1)
