from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
TEMPLATE_NAME = "taxi/manufacturer_list.html"
CONTEXT_OBJECT_NAME = "manufacturer_list"
TEST_DATA_1 = {
    "name": "test_manufacturer_1",
    "country": "test_country_1"
}
TEST_DATA_2 = {
    "name": "test_manufacturer_2",
    "country": "test_country_2"
}


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufactures(self):
        Manufacturer.objects.create(**TEST_DATA_1)
        Manufacturer.objects.create(**TEST_DATA_2)
        res = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context[CONTEXT_OBJECT_NAME]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            res, TEMPLATE_NAME
        )

    def test_search_manufactures(self):
        m1 = Manufacturer.objects.create(**TEST_DATA_1)
        m2 = Manufacturer.objects.create(**TEST_DATA_2)
        query = TEST_DATA_1["name"][-5:]

        res = self.client.get(
            MANUFACTURERS_URL, {"name": query}
        )
        self.assertEqual(
            res.context["search_form"].initial["name"], query
        )
        self.assertIn(m1, res.context[CONTEXT_OBJECT_NAME])
        self.assertNotIn(m2, res.context[CONTEXT_OBJECT_NAME])
