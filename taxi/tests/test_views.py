from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicViewsTests(TestCase):
    def test_index(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class PrivateViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.force_login(self.user)

    def test_index_content(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_retrieve_manufacturer_list_with_search(self):
        Car.objects.create(
            model="Test Car",
            manufacturer=Manufacturer.objects.create(
                name="Test Manufacturer",
                country="Test Country"
            )
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Test"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Test Manufacturer")
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )
        manufacturer = Manufacturer.objects.filter(name__icontains="Test")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
