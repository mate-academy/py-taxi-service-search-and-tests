from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse

from taxi.models import Manufacturer

FORMAT_URL = reverse("taxi:manufacturer-list")


class PublicFormatTest(TestCase):
    def test_login_required(self):
        res = self.client.get(FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivetManufacturersList(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestPrivet", password="password"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test1", country="country_test1")
        Manufacturer.objects.create(name="test2", country="country_test2")
        response = self.client.get(FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
