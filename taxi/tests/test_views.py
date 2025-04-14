from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicAccessTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testUser",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):

        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturers(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Bentley", country="UK")

        response = self.client.get(MANUFACTURER_URL, {"name" : "b"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        manufacturer_names = [
            m.name for m in response.context["manufacturer_list"]
        ]
        self.assertIn("BMW", manufacturer_names)
        self.assertIn("Bentley", manufacturer_names)
        self.assertNotIn("Toyota", manufacturer_names)

        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].initial["name"], "b")

    def test_pagination(self):
        for i in range(7):
            Manufacturer.objects.create(
                name=f"TestManufacturer{i}",
                country="CountryTest"
            )

        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

        response_page_2 = self.client.get(MANUFACTURER_URL + "?page=2")
        self.assertEqual(response_page_2.status_code, 200)
        self.assertEqual(len(response_page_2.context["manufacturer_list"]), 2)

    def test_retrieve_cars(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        Car.objects.create(model="X3", manufacturer=manufacturer_1)
        Car.objects.create(model="Corolla", manufacturer=manufacturer_2)

        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_cars(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        Car.objects.create(model="X3", manufacturer=manufacturer_1)
        Car.objects.create(model="Corolla", manufacturer=manufacturer_2)
        Car.objects.create(model="TestModel", manufacturer=manufacturer_2)

        response = self.client.get(CAR_URL, {"model" : "l"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        cars_models = [c.model for c in response.context["car_list"]]
        self.assertIn("Corolla", cars_models)
        self.assertIn("TestModel", cars_models)
        self.assertNotIn("X3", cars_models)

        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].initial["model"], "l")

    def test_search_drivers(self):
        Driver.objects.create_user(
            username="Maria",
            password="testpass123",
            license_number="ADG12345"
        )
        Driver.objects.create_user(
            username="John",
            password="testpass125",
            license_number="ADG12347"
        )
        Driver.objects.create_user(
            username="Camilla",
            password="testpass128",
            license_number="ADG12341"
        )

        response = self.client.get(DRIVER_URL, {"username": "a"})
        self.assertEqual(response.status_code, 200)
        driver_username = [d.username for d in response.context["driver_list"]]
        self.assertIn("Maria", driver_username)
        self.assertIn("Camilla", driver_username)
        self.assertNotIn("John", driver_username)

        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["username"], "a"
        )
