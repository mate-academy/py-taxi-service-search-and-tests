from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Test1", country="USA")
        Manufacturer.objects.create(name="Test2", country="France")
        Manufacturer.objects.create(name="Test3", country="UK")

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturers_response(self):
        response = self.client.get(MANUFACTURERS_URL, {"name": "Test1"})
        self.assertEqual(response.status_code, 200)

    def test_search_return_expected_number_of_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL, {"name": "Te"})
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_if_expected_manufacturer_present_in_search(self):
        response = self.client.get(MANUFACTURERS_URL, {"name": "Test2"})
        expected_string = "Test2"
        self.assertContains(response, expected_string)

    def test_search_without_results(self):
        response = self.client.get(MANUFACTURERS_URL, {"name": "Nonexistent"})
        self.assertEqual(len(response.context["manufacturer_list"]), 0)
