from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class PublicManufacturerTests(TestCase):
    def test_manufacturer_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_login_required(self):
        url = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        url = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="AAA11111"
        )
        self.client.force_login(driver)
        Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        Manufacturer.objects.create(
            name="test1",
            country="test_country1",
        )

    def test_manufacturer_list_view(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())
        )

    def test_manufacturer_search_view(self):
        url = reverse("taxi:manufacturer-list") + "?search=1"
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="1"))
        )
