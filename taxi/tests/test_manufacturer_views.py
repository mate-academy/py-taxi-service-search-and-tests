from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            license_number="TST12345",
        )

    def test_page_available_for_logged_in_user(self):
        self.client.force_login(self.user)
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_page_uses_correct_template(self):
        self.client.force_login(self.user)
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_login_required(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_search_by_name(self):
        self.client.force_login(self.user)
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        skoda = Manufacturer.objects.create(name="Skoda", country="Czechia")

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "BMW"})

        self.assertContains(response, bmw.name)
        self.assertNotContains(response, skoda.name)
