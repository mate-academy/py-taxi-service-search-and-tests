from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicViewTest(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CARS_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test_name1", country="test_country1")
        Manufacturer.objects.create(name="test_name2", country="test_country2")

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        Car.objects.create(model="test_model_1", manufacturer=manufacturer)
        Car.objects.create(model="test_model_2", manufacturer=manufacturer)

        response = self.client.get(CARS_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self):
        get_user_model().objects.create(
            username="test_username1",
            password="test_password1",
            license_number="AAA84930"
        )
        get_user_model().objects.create(
            username="test_username2",
            password="test_password2",
            license_number="AAA93876"
        )

        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_toggle_assign_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        car = Car.objects.create(
            model="test_model_1",
            manufacturer=manufacturer
        )

        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(car in self.user.cars.all())

        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(car in self.user.cars.all())
