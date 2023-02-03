from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

CARS_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicAccessTests(TestCase):
    def test_login_required(self):
        response = [
            self.client.get(CARS_URL),
            self.client.get(DRIVERS_URL),
            self.client.get(MANUFACTURERS_URL)
        ]
        for item in response:
            self.assertNotEqual(item.status_code, 200)


class PrivateAccessTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="user1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Camry",
            manufacturer=manufacturer
        )
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Manufacturer.objects.create(
            name="BMW",
            country="German"
        )
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]), list(manufacturers))

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_drivers(self):
        pass

    def test_retrieve_car_detail(self):
        pass

    def test_retrieve_driver_detail(self):
        pass
