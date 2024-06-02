from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
INDEX_URL = reverse("taxi:index")


class PublishManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_index_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivetManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TES12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        Manufacturer.objects.create(
            name="test1",
            country="test_country1"
        )
        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="test1",
            manufacturer=manufacturer,
        )
        res = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_retrieve_driver_list(self):
        get_user_model().objects.create_user(
            username="test_0",
            password="test523",
            license_number="TEN12345",
        )
        get_user_model().objects.create_user(
            username="test_1",
            password="test234",
            license_number="OEG12346",
        )
        res = self.client.get(DRIVER_URL)
        drivers = get_user_model().objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")
