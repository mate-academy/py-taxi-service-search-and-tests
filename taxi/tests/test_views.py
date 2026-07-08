from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer


DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicDriversTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_detail_required(self):
        res = self.client.get(reverse("taxi:driver-detail", args=(1,)))
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CARS_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_detail_required(self):
        res = self.client.get(reverse("taxi:car-detail", args=(1,)))
        self.assertNotEqual(res.status_code, 200)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriversTest(TestCase):
    def setUp(self) -> None:
        username = "test_user_name"
        password = "testpassword"
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password
        )
        self.client.force_login(self.user)

    def test_retrive_drivers(self):
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

    def test_retrive_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=(self.user.pk,))
        )
        driver = get_user_model().objects.get(pk=self.user.pk,)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["driver"],
            driver
        )


class PrivateCarsTest(TestCase):
    def setUp(self) -> None:
        username = "test_user_name"
        password = "testpassword"
        self.manufacturer = Manufacturer.objects.create(
            name="Test_Name",
            country="Test_Country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password
        )
        self.car.drivers.set([self.user])
        self.client.force_login(self.user)

    def test_retrive_cars(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_retrive_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=(self.car.pk,))
        )
        car = Car.objects.get(id=self.car.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["car"],
            car
        )
