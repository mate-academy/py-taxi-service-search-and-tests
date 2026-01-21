from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_LIST_URL = reverse("taxi:manufacturer-list")
PAGINATION = 5


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="AAA12345",
            first_name="Admin",
            last_name="User",
            password="1qwerty2",
        )
        self.client.force_login(self.user)

        for i in range(0, PAGINATION + 1):
            Manufacturer.objects.create(
                name=f"Test Manufacturer{i}",
                country=f"Test Country{i}"
            )

    def test_get_manufacturers(self):
        response = self.client.get(MANUFACTURERS_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_manufacturers_list(self):
        response = self.client.get(MANUFACTURERS_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers[:PAGINATION]),
        )

    def test_manufacturer_list_response_with_correct_template(self):
        response = self.client.get(MANUFACTURERS_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_ordered_by_name(self):
        response = self.client.get(MANUFACTURERS_LIST_URL)
        man_list = Manufacturer.objects.all().order_by("name")
        manufacturer_context = response.context["manufacturer_list"]

        self.assertEqual(
            list(manufacturer_context),
            list(man_list[: len(manufacturer_context)]),
        )

    def test_create_manufacturer(self):
        name = "Test Create"
        country = "Test Country Create"
        response = self.client.post(
            reverse(
                "taxi:manufacturer-create",
            ),
            {"name": name, "country": country},
        )

        manufacturer = Manufacturer.objects.get(name=name)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(manufacturer.country, country)

    def test_update_manufacturer(self):
        name = "Test Update"
        updated_name = "Updated Name"
        country = "Test Country Update"
        updated_country = "Test Country Update"

        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country,
        )
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update", kwargs={"pk": manufacturer.id}
            ),
            {"name": updated_name, "country": updated_country},
        )
        Manufacturer.objects.get(id=manufacturer.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Manufacturer.objects.get(id=manufacturer.id).name, updated_name
        )

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Delete",
            country="Country Test Delete",
        )
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=manufacturer.id).exists()
        )
