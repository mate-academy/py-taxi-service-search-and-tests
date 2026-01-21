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
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="TOYOTA")
        Manufacturer.objects.create(name="BMW")
        resp = self.client.get(MANUFACTURER_URL)
        self.assertEqual(resp.status_code, 200)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")
