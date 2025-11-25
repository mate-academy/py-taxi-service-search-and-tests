from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car

DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicDriverViewTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testdriver",
            password="testpass123",
            license_number="XYZ789"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertIn("testdriver", str(res.content))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_driver_search_by_username(self):
        get_user_model().objects.create_user(
            username="anotherdriver",
            password="anotherpass123",
            license_number="LMN456"
        )
        get_user_model().objects.create_user(
            username="testdriver2",
            password="testpass456",
            license_number="QRS123"
        )
        res = self.client.get(DRIVER_LIST_URL, {"username": "testdriver2"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("testdriver2", str(res.content))
        self.assertNotIn("anotherdriver", str(res.content))


class PublicCarViewTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testdriver",
            password="testpass123",
            license_number="XYZ789"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        Manufacturer.objects.create(name="Tesla", country="USA")
        Car.objects.create(model="Model S", manufacturer_id=1)
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/car_list.html")
        self.assertIn("Model S", str(res.content))

    def test_car_search_by_model(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Car.objects.create(model="Corolla", manufacturer_id=1)
        Car.objects.create(model="Camry", manufacturer_id=1)
        res = self.client.get(CAR_LIST_URL, {"model": "Camry"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("Camry", str(res.content))
        self.assertNotIn("Corolla", str(res.content))


class PublicManufacturerViewTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testdriver",
            password="testpass123",
            license_number="XYZ789"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Tesla", country="USA")
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")
        self.assertIn("Tesla", str(res.content))

    def test_manufacturer_search_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "Ford"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("Ford", str(res.content))
        self.assertNotIn("Toyota", str(res.content))
