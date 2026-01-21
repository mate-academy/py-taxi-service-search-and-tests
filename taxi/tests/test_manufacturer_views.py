from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerViewTest(TestCase):
    def test_login_required_manufacturer(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test", country="Ukraine")
        Manufacturer.objects.create(name="Test2", country="The UK")
        res = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
