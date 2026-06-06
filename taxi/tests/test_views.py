from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        for index in range(7):
            Manufacturer.objects.create(
                name=f"Manufacturer {index}",
                country="Germany"
            )

    def setUp(self):
        self.client.force_login(self.user)

    def test_manufacturer_list_view_status_code(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_view_pagination(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(len(response.context["manufacturer_list"]), 5)
