from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicManufacturerTest(TestCase):
    def test_list_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_create_login_required(self):
        res = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_update_delete_login_required(self):
        Manufacturer.objects.create(
            name="Test_name",
            country="Test_country"
        )
        res = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": 1}
        ))
        self.assertNotEqual(res.status_code, 200)

        res = self.client.get(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": 1}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(
            name="Test_name1",
            country="Test_country"
        )
        Manufacturer.objects.create(
            name="Test_name2",
            country="Test_country"
        )
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_get_content_data(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertIsInstance(
            res.context["search_form"],
            ManufacturerSearchForm
        )

    def test_search_form_queryset(self):
        for num in range(10):
            Manufacturer.objects.create(
                name=f"Test_name{num}",
                country="Test_country"
            )
        res = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": "Test_name7"}
        )
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="Test_name7"))
        )

    def test_create_view(self):
        self.client.post(
            MANUFACTURER_CREATE_URL,
            {"name": "Test_name", "country": "Test_country"}
        )
        self.assertTrue(Manufacturer.objects.get(name="Test_name"))

    def test_update_view(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_name",
            country="Test_country"
        )
        update_url = reverse(
            "taxi:manufacturer-update", args=[manufacturer.id]
        )
        res = self.client.post(
            update_url,
            {
                "name": "Test_name_changed",
                "country": "Test_country_changed"
            }
        )
        self.assertEqual(res.status_code, 302)
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.country, "Test_country_changed")
