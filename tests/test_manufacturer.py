from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class PublicManufacturerTests(TestCase):
    def test_manufacturer_list_login_required(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_create_login_required(self):
        url = reverse("taxi:manufacturer-create")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_update_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        url = reverse("taxi:manufacturer-update", args=[manufacturer.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_delete_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        url = reverse("taxi:manufacturer-delete", args=[manufacturer.id])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_manufacturer_search_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Honda", country="Japan")

        url = reverse("taxi:manufacturer-list") + "?name=a"
        response = self.client.get(url)

        manufacturers_contains_a = Manufacturer.objects.filter(
            name__icontains="a"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers_contains_a)
        )

    def test_manufacturer_create(self):
        data = {
            "name": "Toyota",
            "country": "Japan",
        }
        url = reverse("taxi:manufacturer-create")
        response = self.client.post(url, data=data)

        self.assertEqual(Manufacturer.objects.last().name, "Toyota")
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_manufacturer_update(self):
        manufacturer = Manufacturer.objects.create(
            name="Hyundai",
            country="Korea"
        )
        data = {
            "name": "Hyundai",
            "country": "South Korea",
        }
        url = reverse("taxi:manufacturer-update", args=[manufacturer.id])
        response = self.client.post(url, data=data)

        self.assertEqual(Manufacturer.objects.get(
            id=manufacturer.id).country, "South Korea")
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

    def test_manufacturer_delete(self):
        manufacturer = Manufacturer.objects.create(
            name="Hyundai",
            country="Korea"
        )
        url = reverse("taxi:manufacturer-delete", args=[manufacturer.id])
        response = self.client.post(url)

        manufacturers = Manufacturer.objects.all()

        self.assertFalse(manufacturer in manufacturers)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
