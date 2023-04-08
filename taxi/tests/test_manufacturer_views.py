from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="TestUser",
            password="Password",
            license_number="ABC12345"
        )

        cls.manufacturer1 = Manufacturer.objects.create(name="Ford")
        cls.manufacturer2 = Manufacturer.objects.create(name="Toyota")
        cls.manufacturer3 = Manufacturer.objects.create(name="Chevrolet")
        cls.manufacturer4 = Manufacturer.objects.create(name="Honda")
        cls.manufacturer5 = Manufacturer.objects.create(name="Nissan")

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_manufacturer_list_view(self):
        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_view_with_search(self):
        response = self.client.get(MANUFACTURERS_URL, {"name": "o"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ford")
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Honda")
        self.assertContains(response, "Chevrolet")
        self.assertNotContains(response, "Nissan")

    def test_manufacturer_update_view(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                kwargs={"pk": self.manufacturer1.pk}
            ),
            {"name": "Ford Motors", "country": "USA"},
        )

        self.assertEqual(response.url, MANUFACTURERS_URL)
        self.assertEqual(Manufacturer.objects.count(), 5)
        self.assertEqual(
            Manufacturer.objects.get(pk=self.manufacturer1.pk).name,
            "Ford Motors"
        )

    def test_manufacturer_delete_view(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                kwargs={"pk": self.manufacturer1.pk}
            ),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.count(), 4)
        self.assertFalse(
            Manufacturer.objects.filter(pk=self.manufacturer1.pk).exists()
        )

    def test_manufacturer_create_view(self):
        form_data = {"name": "Kia", "country": "Second"}
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            data=form_data,
        )
        manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.count(), 6)
        self.assertEqual(manufacturer.name, "Kia")
