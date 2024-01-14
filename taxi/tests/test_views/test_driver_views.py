from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Car, Manufacturer


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser1",
            password="testpassword123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry"
        )
        self.client = Client()

    def test_driver_list_view_with_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser1")

    def test_driver_list_view_without_login(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("taxi:driver-list")
        )

    def test_get_queryset_with_model_parameter(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(
            "taxi:driver-list"),
            {"username": "testuser1"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser1")

    def test_get_queryset_without_model_parameter(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser1")
