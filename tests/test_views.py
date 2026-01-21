from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")

class PublicManufacturersTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(res.status_code, 200)

class PrivateManufacturersTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Manufacturer 1")
        Manufacturer.objects.create(name="Manufacturer 2")
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Tesla")

        response = self.client.get(MANUFACTURERS_URL, {"name": "BMW"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            [Manufacturer.objects.get(name="BMW")],
            transform=lambda x: x
        )

        response = self.client.get(MANUFACTURERS_URL, {"name": "Tes"})
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertContains(response, "Tesla")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CARS_URL)
        self.assertNotEqual(res.status_code, 200)

class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="Manufacturer 1")
        Car.objects.create(model="Car 1", manufacturer=manufacturer)
        Car.objects.create(model="Car 2", manufacturer=manufacturer)
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car(self):
        manufacturer = Manufacturer.objects.create(name="Audi")
        Car.objects.create(model="q4", manufacturer=manufacturer)
        Car.objects.create(model="m5", manufacturer=manufacturer)
        Car.objects.create(model="v1", manufacturer=manufacturer)

        response = self.client.get(CARS_URL, {"model": "q4"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            [Car.objects.get(model="q4")],
            transform=lambda x: x
        )

        response = self.client.get(CARS_URL, {"model": "q"})
        self.assertContains(response, "q4")
        self.assertNotContains(response, "m5")

class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)
        self.assertNotEqual(res.status_code, 200)

class PrivateDriverTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(username="Driver 1", license_number="test1")
        Driver.objects.create(username="Driver 2", license_number="test2")
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver(self):

        Driver.objects.create(username="Driver 1", license_number="test1")
        Driver.objects.create(username="Driver 2", license_number="test2")
        Driver.objects.create(username="Driver 3", license_number="test3")

        response = self.client.get(DRIVERS_URL, {"username": "Driver 1"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            [Driver.objects.get(username="Driver 1")],
            transform=lambda x: x
        )

        response = self.client.get(DRIVERS_URL, {"username": "1"})
        self.assertContains(response, "Driver 1")
        self.assertNotContains(response, "Driver 2")

    def test_create_driver(self):
        form_data = {
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABC12345",
            "username": "test_username",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])