from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        self.assertNotEqual(self.client.get(MANUFACTURER_URL).status_code, 200)


class PrivateLiteraryFormatTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="BMW")
        self.response = self.client.get(MANUFACTURER_URL)

    def test_request_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_contains_template(self):
        self.assertTemplateUsed(self.response, "taxi/manufacturer_list.html")

    def test_view_contain_objects(self):
        self.assertEqual(
            list(self.response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()),
        )
