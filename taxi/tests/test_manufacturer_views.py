from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerViewsTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="papajoe",
            password="$ecreT_550",
            license_number="MAN99901"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Bumga Gamga",
            country="Poltava"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Gamga Upapu",
            country="Yalta"
        )

    def test_manufacturer_list_url_response(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_has_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        all_manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(all_manufacturers)
        )

    def test_manufacturer_search_form_exists(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertContains(response, "Search by name")
