from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        """
        Checking possibility for non-login user have access to
        Manufacturer-list working LoginRequiredMixin
        for ManufacturerListView
        :return:
        """
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerFormat(TestCase):
    def setUp(self) -> None:
        number_of_manufacturers = 7

        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
        )
        self.client.force_login(self.user)

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Test-name {manufacturer_id}",
                country=f"Test-country {manufacturer_id}",
            )

    def test_retrieve_manufacture_formats(self):
        """
        Checking access login user to ManufacturerListView page
        """
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer_formats = Manufacturer.objects.all()[:5]
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_formats),
        )
        # checking url path to taxi/manufacturer_list.html
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination_is_five(self):
        response = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_lists_all_manufactures(self):
        # Get second page and confirm it has (exactly) remaining 2 items
        response = self.client.get(MANUFACTURER_FORMAT_URL + "?name=&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 2)
