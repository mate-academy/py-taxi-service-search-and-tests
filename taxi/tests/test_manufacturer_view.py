from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123456",
            first_name="test",
            last_name="test"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(response.status_code, 200)
