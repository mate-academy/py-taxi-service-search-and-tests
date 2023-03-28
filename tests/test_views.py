from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test1234567",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test1")
        Manufacturer.objects.create(name="test2")

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="BMW", country="test2")
        response = self.client.get(MANUFACTURER_URL + "?name=bmw")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTests(TestCase):
    def test_car_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test2",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test3",
            country="test4"
        )
        Car.objects.create(model="test1", manufacturer=manufacturer)
        Car.objects.create(model="test2", manufacturer=manufacturer)

        cars = Car.objects.all()
        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="test3",
            country="test4"
        )
        Car.objects.create(model="Yaris", manufacturer=manufacturer)
        response = self.client.get(CAR_URL + "?model=yaris")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTests(TestCase):
    def test_driver_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test2",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        Driver.objects.create(
            username="user",
            password="test1",
            license_number="AAA12345"
        )
        Driver.objects.create(
            username="user1",
            password="test12",
            license_number="AAA23425"
        )
        drivers = Driver.objects.all()
        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search(self):
        Driver.objects.create(
            username="user",
            password="test1",
            license_number="AAA12345"
        )
        response = self.client.get(DRIVER_URL + "?username=user")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
