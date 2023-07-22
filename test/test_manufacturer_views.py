from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import (
    Car,
    Manufacturer,
    Driver
)


class PublicManufacturerViewsTests(TestCase):

    def test_login_required_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_manufacturer_create(self):
        response = self.client.get(
            reverse("taxi:manufacturer-create")
        )
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_manufacturer_update(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", args=[1])
        )
        self.assertNotEquals(response.status_code, 200)


class PrivateCarViewsTests(TestCase):
    def setUp(self):

        self.user1 = get_user_model().objects.create_user(
            username="vasyl",
            password="password123",
            license_number="CBA54321"
        )
        self.user2 = get_user_model().objects.create_user(
            username="petro",
            password="password123",
            license_number="ABC12345"
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="test1",
            country="losos"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="test2",
            country="corop"
        )
        self.car1 = Car.objects.create(
            model="test1",
            manufacturer=self.manufacturer1,
        )
        self.car1.drivers.add(self.user2)
        self.car2 = Car.objects.create(
            model="test2",
            manufacturer=self.manufacturer2,
        )
        self.car2.drivers.add(self.user1)
        self.client.force_login(self.user1)

    def test_retrieve_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(
                response.context["manufacturer_list"]
            ), list(manufacturers)
        )

    def test_manufacturer_search_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(f"{url}?name=test1")
        self.assertIn(
            self.manufacturer1, list(
                response.context["manufacturer_list"]
            )
        )
        self.assertNotIn(
            self.manufacturer2, list(
                response.context["manufacturer_list"]
            )
        )

    def test_manufacturer_update_view(self):
        manufacturer_data = {
            "name": "test3",
            "country": "oseledec"
        }

        url = reverse("taxi:manufacturer-update", args=[self.manufacturer1.id])
        response = self.client.post(url, manufacturer_data)

        self.manufacturer1.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.manufacturer1.name, "test3")
        self.assertEqual(self.manufacturer1.country, "oseledec")

    def test_manufacturer_create_view(self):
        manufacturer_data = {
            "name": "test3",
            "country": "oseledec"
        }
        url = reverse("taxi:manufacturer-create")

        response = self.client.post(url, manufacturer_data)

        self.assertEqual(response.status_code, 302)

        created_manufacturer = Manufacturer.objects.last()

        self.assertEqual(created_manufacturer.name, manufacturer_data["name"])
        self.assertEqual(
            created_manufacturer.country, manufacturer_data["country"]
        )

    def test_manufacturer_delete(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer1.id).exists()
        )
