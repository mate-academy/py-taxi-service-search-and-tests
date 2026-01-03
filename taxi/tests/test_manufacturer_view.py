from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test username",
            password="Pass1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)
        Manufacturer.objects.create(name="test name 1", country="c1")
        Manufacturer.objects.create(name="test name 2", country="c2")
        Manufacturer.objects.create(name="other name", country="c2")

    def test_retrieve_all_manufacturers(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "test"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "test name 1")
        self.assertContains(res, "test name 2")
        self.assertNotContains(res, "other name")
