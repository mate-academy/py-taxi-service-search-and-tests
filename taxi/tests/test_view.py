from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver

URLS = [
    "taxi:manufacturer-list",
    "taxi:car-list",
    "taxi:driver-list"
]


class PublicAccessTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        for url in URLS:
            response = self.client.get(reverse(url))
            self.assertNotEqual(response.status_code, 200)


class PrivateAccessTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345"
        )
        self.client.force_login(self.user)

    def test_login_possibilities(self):
        for data in range(3):
            Driver.objects.create(
                username=f"test{data}",
                password="12345",
                license_number=f"AAA0000{data}"
            )
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        driver_list = response.context["driver_list"]
        self.assertEqual(len(drivers), len(driver_list))
        for driver in drivers:
            self.assertIn(driver, driver_list)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
