from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="panjaby",
            password="lkj456_&^%",
            first_name="Radj",
            last_name="Mallah",
            license_number="OIU78543"
        )
        self.url = reverse("taxi:manufacturer-list")
        self.client.force_login(self.driver)

        self.man1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.man2 = Manufacturer.objects.create(name="Tesla", country="USA")
        self.man3 = Manufacturer.objects.create(
            name="Tata Motors", country="India"
        )

    def test_search(self):
        response = self.client.get(self.url, {"name": "ta"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tata Motors")
        self.assertNotContains(response, "Tesla")

    def test_manufacturers_list_without_searching(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tesla")
        self.assertContains(response, "Tata Motors")
