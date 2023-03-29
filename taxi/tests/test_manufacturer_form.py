from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Paul",
            license_number="KIA19754",
            first_name="Paul",
            last_name="Maslov",
            password="Platina07",
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-create",
            ),
            {"name": "Ford Otosan", "country": "Turkey"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.get(id=1).name, "Ford Otosan")

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Ford Otosan",
            country="Turkey",
        )
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update", kwargs={"pk": manufacturer.id}
            ),
            {"name": "Chrysler", "country": "USA"},
        )
        Manufacturer.objects.get(id=manufacturer.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Manufacturer.objects.get(id=manufacturer.id).name, "Chrysler"
        )

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Chrysler",
            country="USA",
        )
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=manufacturer.id).exists()
        )
