from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer


class ManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="zuzfhan",
            password="abC123!@#",
            first_name="Arjun",
            last_name="Singh",
            license_number="XYZ98765"
        )
        self.url = reverse("taxi:manufacturer-list")
        self.client.force_login(self.driver)
        self.man1 = Manufacturer.objects.create(name="Honda", country="Japan")
        self.man2 = Manufacturer.objects.create(name="Rivian", country="USA")
        self.man3 = Manufacturer.objects.create(
            name="Mahindra", country="India"
        )

    def test_search(self):
        response = self.client.get(self.url, {"name": "ha"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Honda")
        self.assertContains(response, "Mahindra")
        self.assertNotContains(response, "Rivian")

    def test_manufacturers_list_without_searching(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Honda")
        self.assertContains(response, "Rivian")
        self.assertContains(response, "Mahindra")
