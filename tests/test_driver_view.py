from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

DRIVERS_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_when_user_logout(self):
        response = self.client.get(DRIVERS_URL)
        self.assertRedirects(response, f"{reverse('login')}?next=/drivers/")


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="test_username",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="TST12345",
        )

        response = self.client.get(DRIVERS_URL)

        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_on_drivers_list_page(self):
        Driver.objects.create(
            username="test_username123",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="TST12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "test_username123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(
                username__icontains="test_username123")
            ),
        )
