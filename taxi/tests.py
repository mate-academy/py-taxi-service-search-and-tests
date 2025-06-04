from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="user",
            password="testpass123"
        )
        self.client.login(username="user", password="testpass123")

        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Tesla")
        Manufacturer.objects.create(name="BMW")

    def test_search_manufacturers_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Tes"
        )
        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(manufacturers.count(), 1)
        self.assertEqual(manufacturers[0].name, "Tesla")


class DriverListViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="pass1234"
        )
        self.client.login(
            username="testuser",
            password="pass1234"
        )

    def test_search_username_filtering(self):
        response = self.client.get(
            reverse(
                "taxi:driver-list"
            ), {
                "username": "driver1"
            }
        )
        self.assertEqual(response.status_code, 200)

        drivers = response.context["driver_list"]
        for driver in drivers:
            self.assertIn("driver1", driver.username)


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="pass1234"
        )
        self.client.login(username="testuser", password="pass1234")
        manufacturer = Manufacturer.objects.create(name="Toyota")
        for car in range(10):
            Car.objects.create(model=f"Model{car}", manufacturer=manufacturer)

    def test_search_model_filtering(self):
        response = self.client.get(reverse(
            "taxi:car-list"
        ), {
            "model": "Model1"
        }
        )
        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]
        for car in cars:
            self.assertIn("Model1", car.model)

# Create your tests here.
