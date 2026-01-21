from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        manufacturer = self.client.get(MANUFACTURER_URL)
        car = self.client.get(CAR_URL)
        driver = self.client.get(DRIVER_URL)
        self.assertNotEqual(manufacturer.status_code, 200)
        self.assertNotEqual(car.status_code, 200)
        self.assertNotEqual(driver.status_code, 200)


class PrivateManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testPASSWORD",
        )
        self.client.force_login(self.user)

    def test_retrive_manufacturer(self):
        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Suzuki")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
