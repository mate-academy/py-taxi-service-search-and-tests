from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicSearchTests(TestCase):
    def test_login_required_for_search(self):
        res_manufacturers = self.client.get(reverse("taxi:manufacturer-list"))
        res_cars = self.client.get(reverse("taxi:car-list"))
        res_drivers = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(res_manufacturers.status_code, 200)
        self.assertNotEqual(res_cars.status_code, 200)
        self.assertNotEqual(res_drivers.status_code, 200)


class PrivateSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123",
            license_number="TST12345"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

        res = self.client.get(reverse("taxi:manufacturer-list") + "?name=toy")

        self.assertEqual(res.status_code, 200)
        manufacturers = res.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "Toyota")

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        Car.objects.create(model="Model S", manufacturer=manufacturer)
        Car.objects.create(model="Corolla", manufacturer=manufacturer)

        res = self.client.get(reverse("taxi:car-list") + "?model=mod")

        self.assertEqual(res.status_code, 200)
        cars = res.context["car_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Model S")

    def test_search_driver_by_username(self):
        get_user_model().objects.create_user(
            username="john_doe",
            password="password123",
            license_number="JOH12345"
        )

        res = self.client.get(reverse("taxi:driver-list") + "?username=john")

        self.assertEqual(res.status_code, 200)
        drivers = res.context["driver_list"]
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "john_doe")
