from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicViewsTests(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(  # type: ignore
            username="test",
            password="testpass123454565"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="ZAZ", country="Ukraine")

        response = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
