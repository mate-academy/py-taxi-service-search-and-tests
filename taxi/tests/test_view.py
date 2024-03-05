from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car

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
            self.assertNotEquals(response.status_code, 200)


class PrivateAccessTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Test123"
        )
        self.client.force_login(self.user)

    def test_login_possabilities(self):
        for i in range(3):
            Driver.objects.create(
                username=f"test{i}",
                password="some123",
                license_number=f"ABC1234{i}"
            )
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEquals(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEquals(len(drivers), len(response.context["driver_list"]))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
