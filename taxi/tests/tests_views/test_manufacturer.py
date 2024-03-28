from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver


class LoginRequiredManufacturerViewTest(TestCase):
    def test_login_required_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_manufacturer_create(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_manufacturer_update(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_manufacturer_delete(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)


class ManufacturerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 4
        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Test{manufacturer_id}",
                country=f"Country{manufacturer_id}"
            )

    def setUp(self):
        driver = Driver.objects.create(
            username="Test1",
            password="12345",
            license_number="ABC12345"
        )
        self.client.force_login(driver)
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

    def test_list_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        drivers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(
            response.context["manufacturer_list"]),
            list(drivers)
        )

    def test_filter_list_manufacturers(self):
        response = self.client.get(f"{reverse("taxi:driver-list")}?name=1")
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_pagination_list_manufacturers(self):
        for manufacturer_id in range(8):
            Manufacturer.objects.create(
                name=f"Test2{manufacturer_id}",
                country=f"Country2{manufacturer_id}"
            )
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

        response = self.client.get(
            f"{reverse("taxi:manufacturer-list")}?name=2&page=2"
        )
        self.assertEqual(response.context["paginator"].num_pages, 2)
        self.assertEqual(len(response.context["manufacturer_list"]), 4)

    def test_manufacturer_create_get(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Name")
        self.assertContains(response, "Country")

    def test_manufacturer_create_post(self):
        data = {
            "name": "BMW",
            "country": "Germany"
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=data)
        new_manufacturer = Manufacturer.objects.get(name=data["name"])
        self.assertEqual(new_manufacturer.country, data["country"])

    def test_manufacturer_update_get(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)
        self.assertContains(response, self.manufacturer.country)

    def test_manufacturer_update_post(self):
        data = {
            "name": "Audi888",
            "country": "Germany"
        }
        self.client.post(reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer.id}
        ), data=data)
        new_manufacturer = Manufacturer.objects.get(name=data["name"])
        self.assertEqual(new_manufacturer.country, data["country"])

    def test_manufacturer_delete_get(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete manufacturer?")

    def test_manufacturer_delete_post(self):
        self.client.post(reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": self.manufacturer.id}
        ))
        ls = Manufacturer.objects.filter(name=self.manufacturer.name)
        self.assertEqual(len(ls), 0)
