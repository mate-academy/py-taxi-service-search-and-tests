from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PrivateManufacturerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 23

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Manufacturer {manufacturer_id}",
                country=f"Country {manufacturer_id}",
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
        self.assertEqual(
            list(
                response.context["manufacturer_list"]
            ),
            list(manufacturers)[:5],
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturers_second_page(self):
        response = self.client.get(MANUFACTURERS_URL + "?page=5")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_retrieve_manufacturers_search(self):
        response = self.client.get(MANUFACTURERS_URL + "?name=2")
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.filter(name__icontains=2)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturer)
        )

        response = self.client.get(MANUFACTURERS_URL + "?page=2&name=1")
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.filter(name__icontains=1)
        self.assertEqual(
            list(
                response.context["manufacturer_list"]
            ),
            list(manufacturer)[5:10]
        )

    def test_create_manufacturer(self):
        form_data = {"name": "Test", "country": "Test"}
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_update_manufacturer(self):
        form_data = {"name": "UpdatedName", "country": "NewCountry"}
        self.client.post(
            reverse("taxi:manufacturer-update", args=[1]),
            data=form_data,
        )
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_delete_car_get_request(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", args=[1]), follow=True
        )
        self.assertContains(response, "Delete manufacturer?")

    def test_delete_car_post_request(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[1]), follow=True
        )
        self.assertRedirects(
            response, reverse("taxi:manufacturer-list"), status_code=302
        )
