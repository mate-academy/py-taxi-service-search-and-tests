from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import SearchForm
from taxi.models import Manufacturer

URL_MANUFACTURER_LIST = reverse("taxi:manufacturer-list")
URL_MANUFACTURER_CREATE = reverse("taxi:manufacturer-create")


class PublicManufacturerView(TestCase):
    def test_manufacturer_list_login_required(self):
        response = self.client.get(URL_MANUFACTURER_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        response = self.client.get(URL_MANUFACTURER_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_update_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        url_update = reverse(
            "taxi:manufacturer-update", args=[manufacturer.id]
        )
        res_update = self.client.get(url_update)
        self.assertNotEqual(res_update.status_code, 200)

        url_delete = reverse(
            "taxi:manufacturer-delete", args=[manufacturer.id]
        )
        res_delete = self.client.get(url_delete)
        self.assertNotEqual(res_delete.status_code, 200)


class PrivateManufacturerTestListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
        )

        self.client.force_login(self.user)

    def test_manufacturer_login_required(self):
        response = self.client.get(URL_MANUFACTURER_LIST)
        self.assertEqual(response.status_code, 200)

    def test_context_data_list(self):
        response = self.client.get(URL_MANUFACTURER_LIST)
        self.assertIsInstance(response.context["form_search"], SearchForm)

    def test_manufacturer_list_search(self):
        for index in range(5):
            Manufacturer.objects.create(
                name=f"test{index}",
                country=f"country_test{index}"
            )
        response = self.client.get(
            URL_MANUFACTURER_LIST, {"search_field": "test1"}
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="test1"))
        )

    def test_manufacturer_create_view(self):
        self.client.post(
            URL_MANUFACTURER_CREATE,
            {
                "name": "test1", "country": "test_country1"
            }
        )
        self.client.post(
            URL_MANUFACTURER_CREATE,
            {
                "name": "test3", "country": "test_country5"
            }
        )
        self.assertTrue(Manufacturer.objects.get(name="test1"))
        self.assertTrue(Manufacturer.objects.get(name="test3"))

    def test_manufacturer_update_view(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        url_update = reverse(
            "taxi:manufacturer-update", args=[manufacturer.id]
        )
        response = self.client.post(
            url_update, {"name": "test_name", "country": "test_country_change"}
        )

        self.assertEqual(response.status_code, 302)
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.country, "test_country_change")
