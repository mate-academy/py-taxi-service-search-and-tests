from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="test_password",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="General Motors", country="USA")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Toyota Prado", country="Japan")
        Manufacturer.objects.create(name="Toyota Camry", country="Japan")
        Manufacturer.objects.create(name="Suzuki", country="Japan")

    def test_manufacturer_retrieve_list_view(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(manufacturers),
            list(response.context["manufacturer_list"])
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_form_in_manufacturer(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota Prado")
        self.assertContains(response, "Toyota Camry")
        self.assertNotContains(response, "Suzuki")
        self.assertNotContains(response, "General Motors")
