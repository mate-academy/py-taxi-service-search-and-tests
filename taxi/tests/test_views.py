from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class PrivateManufacturerTest(TestCase):
    MANUFACTURER_URL = reverse("taxi:manufacturer-list")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="man1", country="country1")
        Manufacturer.objects.create(name="cat1", country="country2")

    def test_retrieve_manufacturers(self):
        response = self.client.get(self.MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturers_search(self):
        criteria = "cat"
        response = self.client.get(self.MANUFACTURER_URL + f"?name={criteria}")
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.filter(name__icontains=criteria)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )


class PrivateCarTest(TestCase):
    CAR_URL = reverse("taxi:car-list")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(name="manufacturer",
                                                   country="country1")
        Car.objects.create(model="car", manufacturer=manufacturer)
        Car.objects.create(model="notcar", manufacturer=manufacturer)

    def test_retrieve_cars(self):
        response = self.client.get(self.CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_cars_search(self):
        criteria = "not"
        response = self.client.get(self.CAR_URL + f"?model={criteria}")
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.filter(model__icontains=criteria)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )


class PrivateDriverTest(TestCase):
    DRIVER_URL = reverse("taxi:driver-list")

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        common_test_data = {
            "last_name": "TestLast",
            "password": "qwerty123"
        }
        Driver.objects.create_user(
            **common_test_data,
            first_name="Kevin",
            username="username1",
            license_number="ABC12345"
        )
        Driver.objects.create_user(
            **common_test_data,
            first_name="Mike",
            username="username2",
            license_number="DFR98765"
        )

    def test_retrieve_drivers(self):
        response = self.client.get(self.DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_drivers_search(self):
        criteria = "ike"
        response = self.client.get(self.DRIVER_URL + f"?first_name={criteria}")
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.filter(first_name__icontains=criteria)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
