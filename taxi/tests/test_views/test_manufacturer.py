from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer


class PrivateManufacturerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="test",
            password="test12345",
            first_name="first_test",
            last_name="last_test",
            license_number="ABC12345",
        )
        cls.manufacturer_1 = Manufacturer.objects.create(
            name="test_manufacturer1",
            country="test_country1"
        )
        cls.manufacturer_2 = Manufacturer.objects.create(
            name="test_manufacturer2",
            country="test_country2"
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        query = "test_manufacturer1"
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            data={"q": query}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.manufacturer_1, response.context["object_list"])
        self.assertNotIn(self.manufacturer_2, response.context["object_list"])
