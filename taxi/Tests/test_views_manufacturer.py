from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_user_manufacturer(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Toyota")
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )


class ManufacturerCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        manufacturer_count_before = Manufacturer.objects.count()
        response = self.client.post(reverse(
            "taxi:manufacturer-create"
        ),
            data={
                "name": "Ford",
                "country": "USA"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.count(), manufacturer_count_before + 1)


class ManufacturerUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_update_manufacturer(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer.pk}
            ),
            data={
                "name": "Toyota Motors",
                "country": "Japan"
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
        self.manufacturer.refresh_from_db()
        self.assertEqual(
            self.manufacturer.name, "Toyota Motors"
        )


class ManufacturerDeleteTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_delete_manufacturer(self):
        manufacturer_count_before = Manufacturer.objects.count()
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": self.manufacturer.pk}
            )
        )
        self.assertEqual(
            response.status_code, 302
        )
        self.assertEqual(
            Manufacturer.objects.count(),
            manufacturer_count_before - 1
        )
