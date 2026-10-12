from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Mercedes")
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_list.html"
        )

    def test_search_manufacturers_by_name(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Mercedes")
        Manufacturer.objects.create(name="Toyota")

        res = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": "bmw"},
        )

        self.assertEqual(res.status_code, 200)
        self.assertQuerySetEqual(
            res.context["manufacturer_list"],
            ["BMW"],
            transform=lambda manufacturer: manufacturer.name,
        )

    def test_manufacturer_list_pagination(self):
        Manufacturer.objects.bulk_create([
            Manufacturer(name=f"Manufacturer {i}", country="Test")
            for i in range(7)
        ])

        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["manufacturer_list"]), 5)
        self.assertTrue(res.context["is_paginated"])

    def test_create_manufacturer(self):
        url = reverse("taxi:manufacturer-create")

        res = self.client.post(url, {
            "name": "Toyota",
            "country": "Japan",
        })

        self.assertRedirects(
            res,
            reverse("taxi:manufacturer-list"),
        )
        self.assertTrue(
            Manufacturer.objects.filter(name="Toyota").exists()
        )

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        url = reverse(
            "taxi:manufacturer-update",
            args=[manufacturer.pk],
        )

        response = self.client.post(url, {
            "name": "BMW Updated",
            "country": "Germany",
        })

        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list"),
        )

        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, "BMW Updated")

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        url = reverse(
            "taxi:manufacturer-delete",
            args=[manufacturer.pk],
        )

        response = self.client.post(url)

        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list"),
        )
        self.assertFalse(
            Manufacturer.objects.filter(pk=manufacturer.pk).exists()
        )


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="X9!qL2#vR7@k",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_driver",
            "password1": "X9!qL2#vR7@k",
            "password2": "X9!qL2#vR7@k",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TVR31245",
        }
        self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(
            new_driver.first_name,
            form_data["first_name"]
        )
        self.assertEqual(
            new_driver.last_name,
            form_data["last_name"]
        )
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )

    def test_search_drivers_by_username(self):
        user1 = get_user_model().objects.create_user(
            username="john_driver",
            password="X9!qL2#vR7@k",
            license_number="TVR31245",
        )

        url = reverse("taxi:driver-list")
        response = self.client.get(
            url,
            {"username": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            [user1]
        )
