from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.create_drivers()

    def create_drivers(self):
        self.driver1 = Driver.objects.create(
            username="new_user",
            password="password",
            first_name="John",
            last_name="Doe",
            license_number="AVB12345"
        )
        self.driver2 = Driver.objects.create(
            username="new_user1",
            password="password1",
            first_name="Test1",
            last_name="Test",
            license_number="AHB12345"
        )
        self.driver3 = Driver.objects.create(
            username="search_user2",
            password="password2",
            first_name="Jane",
            last_name="Smith",
            license_number="CHC12345"
        )

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_search_driver(self):
        search_term = "John"
        response = self.client.get(DRIVER_URL, {"username": search_term})
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.filter(username__icontains=search_term)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
