from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST = reverse("taxi:manufacturer-list")
CARS_LIST = reverse("taxi:car-list")
DRIVERS_LIST = reverse("taxi:driver-list")


class PublicViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="TeJus2pwd",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test-country"
        )
        self.car = Car.objects.create(
            model="test_car",
            manufacturer=self.manufacturer,
        )

    def test_login_required_manufacturer(self):
        res = self.client.get(MANUFACTURER_LIST)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car(self):
        res = self.client.get(CARS_LIST)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver(self):
        res = self.client.get(DRIVERS_LIST)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_detail(self):
        res = self.client.get(
            reverse(
                "taxi:driver-detail",
                args=[self.user.id])
        )
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_detail(self):
        res = self.client.get(reverse("taxi:car-detail", args=[self.car.id]))
        self.assertNotEqual(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Querty123"
        )
        self.manufacture1 = Manufacturer.objects.create(
            name="test",
            country="test-country"
        )
        self.manufacture2 = Manufacturer.objects.create(
            name="test2",
            country="test-country2"
        )
        self.car = Car.objects.create(
            model="test model",
            manufacturer=self.manufacture1
        )
        self.car.drivers.add(self.user)
        self.client.force_login(self.user)

    def test_users_access_to_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST)
        self.assertEqual(response.status_code, 200)

    def test_users_access_to_cars_list(self):
        response = self.client.get(CARS_LIST)
        self.assertEqual(response.status_code, 200)

    def test_users_access_to_drivers_list(self):
        response = self.client.get(DRIVERS_LIST)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturer_list(self):
        manufacturer_list = Manufacturer.objects.all()
        response = self.client.get(MANUFACTURER_LIST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_car_list(self):
        cars_list = Car.objects.all()
        response = self.client.get(CARS_LIST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars_list)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers_list(self):
        drivers_list = get_user_model().objects.all()
        response = self.client.get(DRIVERS_LIST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers_list)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
