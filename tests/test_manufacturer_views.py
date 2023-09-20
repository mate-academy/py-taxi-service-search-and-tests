from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_LIST_VIEW = "/manufacturers/"
MANUFACTURER_CREATE_VIEW = "/manufacturers/create/"
MANUFACTURER_UPDATE_VIEW = "/manufacturers/1/update/"
MANUFACTURER_DELETE_VIEW = "/manufacturers/1/delete/"


class PublicManufacturerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Mercedes", country="Germany")

    def test_manufacturer_list_page_requires_login(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_page_requires_login(self):
        response = self.client.get(MANUFACTURER_CREATE_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_page_requires_login(self):
        response = self.client.get(MANUFACTURER_UPDATE_VIEW)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_page_requires_login(self):
        response = self.client.get(MANUFACTURER_DELETE_VIEW)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Mercedes", country="Germany")
        Manufacturer.objects.create(name="Volkswagen", country="Germany")

    def setUp(self) -> None:
        user = get_user_model().objects.create(
            username="test_user",
            password="test123user"
        )
        self.client.force_login(user)

    # Test if all the pages are accessible
    def test_retrieve_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW)
        manufacturers_list = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers_list)
        )

    def test_retrieve_manufacturer_create_page(self):
        response = self.client.get(MANUFACTURER_CREATE_VIEW)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturer_update_page(self):
        response = self.client.get(MANUFACTURER_UPDATE_VIEW)
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["manufacturer"], manufacturer)

    def test_retrieve_manufacturer_delete_page(self):
        response = self.client.get(MANUFACTURER_DELETE_VIEW)
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["manufacturer"], manufacturer)

    # Test if all the pages are accessible by their name
    def test_retrieve_manufacturer_list_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturer_create_page_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturer_update_page_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturer_delete_page_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", args=[1])
        )
        self.assertEqual(response.status_code, 200)

    def test_search_manufacturer_by_name(self):
        search_field = "name"
        search_value = "volk"
        url = f"{MANUFACTURER_LIST_VIEW}?{search_field}={search_value}"
        response = self.client.get(url)

        expected_queryset = Manufacturer.objects.filter(
            name__icontains=search_value
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]),
            list(expected_queryset)
        )
