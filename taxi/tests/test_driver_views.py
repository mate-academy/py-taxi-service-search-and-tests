from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver

driver_url = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):

    def test_login_required(self):
        res = self.client.get(driver_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverListViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="driver1",
            password="password1",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="driver2",
            password="password2",
            license_number="NBH56487"
        )
        response = self.client.get(driver_url)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
