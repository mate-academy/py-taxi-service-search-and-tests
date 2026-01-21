from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test user",
            password="test123user"
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_get_context_data_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "BMW"})
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial["name"], "BMW")

    def test_get_queryset_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "bmw"})
        manufacturer_names = [
            manufacturer.name
            for manufacturer in response.context["manufacturer_list"]
        ]
        self.assertIn("BMW", manufacturer_names)
        self.assertNotIn("Ford", manufacturer_names)


MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PrivateManufacturerCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test user",
            password="<PASSWORD>"
        )
        self.client.force_login(self.user)

    def test_retrieve_create_manufacturer(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "BMW",
            "country": "Germany",
        }
        response = self.client.post(MANUFACTURER_CREATE_URL, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="BMW").exists())


class PrivateManufacturerUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test user",
            password="<PASSWORD>"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.url = reverse(
            "taxi:manufacturer-update",
            args=[self.manufacturer.id],
        )
        self.client.force_login(self.user)

    def test_retrieve_update_manufacturer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_update_manufacturer(self):
        form_data = {
            "name": "Ford",
            "country": "USA",
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Ford").exists())


class PrivateManufacturerDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test user",
            password="<PASSWORD>"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.url = reverse(
            "taxi:manufacturer-delete",
            args=[self.manufacturer.id],
        )
        self.client.force_login(self.user)

    def test_retrieve_delete_manufacturer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("taxi/manufacturer_confirm_delete.html")

    def test_delete_manufacturer(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(name="BMW").exists())
