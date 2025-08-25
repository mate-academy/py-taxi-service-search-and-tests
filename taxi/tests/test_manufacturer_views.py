from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.models import Manufacturer
from taxi.views import ManufacturerListView

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test123"
        )
        self.client.force_login(self.user)
        self.factory = RequestFactory()

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        Manufacturer.objects.create(
            name="test_name2",
            country="test_country2"
        )
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        manufacturer_data = {
            "name": "test_name",
            "country": "test_country"
        }
        res = self.client.post(
            reverse("taxi:manufacturer-create"),
            manufacturer_data
        )
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Manufacturer.objects.count(), 1)
        self.assertRedirects(res, "/manufacturers/")

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        manufacturer_update = {
            "name": "test_name_update",
            "country": "test_country_update"
        }
        res = self.client.post(
            reverse("taxi:manufacturer-update", args=[manufacturer.pk]),
            manufacturer_update
        )
        self.assertEqual(res.status_code, 302)
        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, "test_name_update")
        self.assertEqual(manufacturer.country, "test_country_update")
        self.assertRedirects(res, "/manufacturers/")

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        res = self.client.post(
            reverse("taxi:manufacturer-delete", args=[manufacturer.pk])
        )
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Manufacturer.objects.count(), 0)
        self.assertRedirects(res, "/manufacturers/")

    def test_get_context_data_manufactory(self):
        Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        Manufacturer.objects.create(
            name="test_name2",
            country="test_country2"
        )
        request = self.factory.get(
            reverse("taxi:manufacturer-list"), {"name": "Test_name2"}
        )
        request.user = self.user

        view = ManufacturerListView()
        view.setup(request)
        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().name, "test_name2")
