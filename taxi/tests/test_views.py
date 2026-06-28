from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Manufacturer


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_creation_user(self):
        self.assertEqual(self.user.username, "user1")

    def test_validation_password(self):
        self.assertTrue(self.user.check_password("test123"))


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="test123",
        )
        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="Honda")
        self.client.force_login(self.user)

    def test_search_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer_list"),
            {"name": "Audi"}
        )

        self.assertContains(response, "Audi")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Honda")
