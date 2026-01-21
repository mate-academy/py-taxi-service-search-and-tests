from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverViewTest(TestCase):
    def test_login_required_driver(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTestView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="username1",
            password="password123",
            license_number="TES12356"
        )
        Driver.objects.create(
            username="username2",
            password="pass65498",
            license_number="HRE45678"
        )
        res = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
