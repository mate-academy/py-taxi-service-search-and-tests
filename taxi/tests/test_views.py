from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicManufacturerListView(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicCarListView(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicDriverListView(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateViewTestBase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)


class PrivateManufacturerListView(PrivateViewTestBase):
    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="Manufacturer 1", country="US")
        Manufacturer.objects.create(name="Manufacturer 2", country="DE")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarListView(PrivateViewTestBase):
    def test_retrieve_car_list(self):
        manufacturer_audi = Manufacturer.objects.create(
            name="Audi",
            country="DE"
        )
        manufacturer_bmw = Manufacturer.objects.create(
            name="BMW",
            country="DE"
        )
        Car.objects.create(model="A4", manufacturer=manufacturer_audi)
        Car.objects.create(model="3", manufacturer=manufacturer_bmw)

        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverListView(PrivateViewTestBase):
    def test_retrieve_driver_list(self):
        get_user_model().objects.create_user(
            username="test1",
            password="test123",
            license_number="AAA111",
        )
        get_user_model().objects.create_user(
            username="test2",
            password="test456",
            license_number="BBB222",
        )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        expected_drivers = list(
            get_user_model().objects.filter(is_superuser=False)
        )
        self.assertQuerySetEqual(
            list(response.context["driver_list"]),
            expected_drivers,
            transform=lambda x: x,
            ordered=False
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
