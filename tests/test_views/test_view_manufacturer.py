from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerFormatTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerFormatTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_manufacturer(self):
        Manufacturer.objects.create(name="test123", country="test"),
        Manufacturer.objects.create(name="tet321", country="test2")

        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)

        manufacturer = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Mustang")
        Manufacturer.objects.create(name="Volkswagen")

        response = self.client.get(MANUFACTURER_URL, data={"param": "Mu"})
        self.assertEqual(response.status_code, 200)
        # print(list(response))

        self.assertContains(response, "Mustang")
        self.assertNotContains(response, "Volkswagen")

    def test_search_manufacturer_name_not_found(self):
        response = self.client.get(MANUFACTURER_URL, data={"param": "GG"})
        self.assertEqual(response.status_code, 200)


class ManufacturerChangeTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Mustang",
            country="USA"
        )

        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_manufacturer_update_redirects_to_success_url(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer.pk}
            ), data={"name": "BMW", "country": "GERMANY"}
        )
        self.assertRedirects(response, MANUFACTURER_URL)

    def test_manufacturer_successful_deletion_redirects_to_success_url(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": self.manufacturer.pk}
            )
        )
        self.assertRedirects(response, MANUFACTURER_URL)
