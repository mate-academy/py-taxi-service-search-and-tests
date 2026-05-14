from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )

    def test_login_required_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create(self):
        res = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_update(self):
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_delete(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            first_name="test",
            password="test",
            last_name="test",
            license_number="TES12345"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="test", country="test")
        Manufacturer.objects.create(name="test1", country="test1")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))
        self.assertTemplateUsed(response,
                                "taxi/manufacturer_list.html")
