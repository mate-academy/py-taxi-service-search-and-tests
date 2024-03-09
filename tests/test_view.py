from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse_lazy("taxi:manufacturer-list")
CARS_URL = reverse_lazy("taxi:car-list")
CARS_CREATE_URL = reverse_lazy("taxi:car-create")
DRIVERS_URL = reverse_lazy("taxi:driver-list")


class PublicManufacturerTests(TestCase):

    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_manufacturer",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Renault_test", country="France_test")
        Manufacturer.objects.create(name="BMW_test", country="Germany_test")

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed("taxi:manufacturer-list")

    def test_create_manufacturer(self):
        form_data = {
            "name": "Renault_test",
            "country": "France_test"
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)

        manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(manufacturer.country, form_data["country"])


class PublicCarTests(TestCase):

    def test_login_required(self):
        res = self.client.get(CARS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_car",
            "password123"
        )

        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="Renault_test",
            country="France_test"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="BMW_test",
            country="Germany_test"
        )
        Car.objects.create(model="X5_test", manufacturer=manufacturer_1)
        Car.objects.create(model="M5_test", manufacturer=manufacturer_2)

        response = self.client.get(CARS_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed("taxi:car-list")

    def test_create_car(self):

        response = self.client.get(CARS_CREATE_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("taxi:car-create")


class PublicDriverTests(TestCase):

    def test_driver_login_required(self):
        res = self.client.get(DRIVERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_driver",
            "password123"
        )

        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="driver1_test",
            license_number="DRI12345"
        )
        Driver.objects.create(
            username="driver2_test",
            license_number="VER56789"
        )

        response = self.client.get(DRIVERS_URL)

        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

        self.assertTemplateUsed("taxi:driver-list")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "license_number": "NUD12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "password1": "user123test",
            "password2": "user123test"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
