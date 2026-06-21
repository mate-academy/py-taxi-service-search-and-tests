from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicAccessTests(TestCase):
    """Анонимный пользователь не должен попадать на list-страницы"""

    def test_login_required_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

    def test_manufacturer_list_without_search_returns_all(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(Manufacturer.objects.all()),
        )

    def test_manufacturer_search_by_full_name(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "Toyota"})
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="Toyota")),
        )

    def test_manufacturer_search_partial_case_insensitive(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "bm"})
        manufacturers = res.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "BMW")

    def test_manufacturer_search_no_match_returns_empty(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "Lada"})
        self.assertEqual(len(res.context["manufacturer_list"]), 0)


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        Car.objects.create(model="Camry", manufacturer=manufacturer)
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="RAV4", manufacturer=manufacturer)

    def test_car_search_by_model_partial(self):
        res = self.client.get(CAR_LIST_URL, {"model": "cam"})
        cars = res.context["car_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Camry")

    def test_car_search_no_results(self):
        res = self.client.get(CAR_LIST_URL, {"model": "Tesla"})
        self.assertEqual(len(res.context["car_list"]), 0)


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_user",
            password="testpass123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        get_user_model().objects.create_user(
            username="john_doe",
            password="testpass123",
            license_number="DEF12345",
        )
        get_user_model().objects.create_user(
            username="jane_smith",
            password="testpass123",
            license_number="GHI12345",
        )

    def test_driver_search_by_username_partial(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": "john"})
        drivers = res.context["driver_list"]
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "john_doe")

    def test_driver_search_empty_returns_all(self):
        res = self.client.get(DRIVER_LIST_URL, {"username": ""})
        self.assertEqual(
            len(res.context["driver_list"]),
            get_user_model().objects.count(),
        )
