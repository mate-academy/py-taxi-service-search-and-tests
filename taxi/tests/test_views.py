from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin1",
            password="Test123321#",
            license_number="XML00000"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="AdMin",
            password="TesT123321#",
            license_number="XML00001"
        )
        Driver.objects.create(
            username="ADMIn",
            password="TEsT123321#",
            license_number="XML00002"
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
