from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admintest",
            password="passwordtest",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="testname", country="testcountry")
        Manufacturer.objects.create(name="testname2", country="testcountry2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["object_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
