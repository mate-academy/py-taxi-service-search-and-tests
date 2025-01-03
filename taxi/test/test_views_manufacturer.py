from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_name_1", country="US"
        )
        Manufacturer.objects.create(name="test_name_2", country="GB")
        self.manufacturer_list_url = reverse("taxi:manufacturer-list")
        self.manufacturer_create_url = reverse("taxi:manufacturer-create")

    def test_retrieve_manufacturer(self):
        response = self.client.get(self.manufacturer_list_url)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        form_data = {"name": "test_name_1"}
        response = self.client.get(self.manufacturer_list_url, data=form_data)
        manufacturers = Manufacturer.objects.all().filter(
            name=form_data["name"]
        )
        self.assertEqual(
            len(response.context["manufacturer_list"]), len(manufacturers)
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {"name": "test_new_name", "country": "test_country_1"}
        self.assertFalse(
            Manufacturer.objects.filter(name=form_data["name"]).exists()
        )

        response = self.client.post(self.manufacturer_create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Manufacturer.objects.filter(name=form_data["name"]).exists()
        )

        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])
        self.assertEqual(new_manufacturer.name, form_data["name"])

    def test_update_manufacturer(self):
        form_data = {"name": "test_update_name", "country": "country_update"}
        url = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.id}
        )
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, form_data["name"])
        self.assertEqual(self.manufacturer.country, form_data["country"])

    def test_delete_manufacturer(self):
        count = Manufacturer.objects.count()
        url = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.id}
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.count() + 1, count)
