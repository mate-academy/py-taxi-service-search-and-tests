from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        res = self.client.get(MANUFACTURER_URL, data={"name": "au"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Audi")
        self.assertNotContains(res, "BMW")


class ManufacturerChangeTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_update_redirect_to_success_url(self):
        res = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer.pk}
            ),
            data={"name": "Audi", "country": "Germany"}
        )
        self.assertRedirects(res, MANUFACTURER_URL)

    def test_manufacturer_delete_redirect_to_success_url(self):
        res = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": self.manufacturer.pk}
            )
        )
        self.assertRedirects(res, MANUFACTURER_URL)
