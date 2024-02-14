from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test", country="test")
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturer)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        driver = Driver.objects.create(license_number="ABC12345")
        manufacturer = Manufacturer.objects.create(
            name="test", country="test"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)

        car.drivers.add(driver)
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        driver = Driver.objects.all()
        self.assertEqual(list(res.context["driver_list"]), list(driver))
        self.assertTemplateUsed(res, "taxi/driver_list.html")
