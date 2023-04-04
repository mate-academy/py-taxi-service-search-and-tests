from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

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

        self.manufacturer = Manufacturer.objects.create(
            name="test3",
            country="test4"
        )

    def test_retrieve_car(self):
        Car.objects.create(model="test1", manufacturer=self.manufacturer)
        Car.objects.create(model="test2", manufacturer=self.manufacturer)

        cars = Car.objects.all()
        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
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


class ToggleAssignToCarViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test2",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(name="test")

    def test_toggle_assign_to_car_driver_is_assigned(self):
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )
        response = self.client.get(reverse(
            "taxi:toggle-car-assign",
            args=[self.car.pk]
        ))
        self.car.drivers.set([self.user])
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.car in self.user.cars.all())

    def test_toggle_assign_to_car_driver_is_not_assigned(self):
        self.driver = Driver.objects.create(
            username="testuser",
            password="testpass",
            license_number="AAA23425"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer
        )
        response = self.client.get(reverse(
            "taxi:toggle-car-assign",
            args=[self.car.pk]
        )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.car in self.driver.cars.all())
