from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car

User = get_user_model()


class ManufacturerSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Tesla", country="USA")

    def setUp(self):
        self.client.login(
            username="testuser",
            password="testpass"
        )

    def test_manufacturer_search_results(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"manufacturer": "Ford"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertEqual(
            response.context["manufacturer_list"][0].name,
            "Ford"
        )

    def test_manufacturer_search_no_results(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"manufacturer": "Honda"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["manufacturer_list"]), 0
        )

    def test_manufacturer_search_partial_match(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"manufacturer": "T"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["manufacturer_list"]), 2
        )
        manufacturers = [
            manufacturer.name for manufacturer
            in response.context["manufacturer_list"]
        ]
        self.assertIn("Toyota", manufacturers)
        self.assertIn("Tesla", manufacturers)


class CarSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )

        Car.objects.create(model="Camry", manufacturer=manufacturer)
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="Civic", manufacturer=manufacturer)

    def setUp(self):
        self.client.login(
            username="testuser",
            password="testpass"
        )

    def test_car_search_results(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"car": "Camry"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(
            response.context["car_list"][0].model, "Camry"
        )

    def test_car_search_no_results(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"car": "Accord"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 0)

    def test_car_search_partial_match(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"car": "C"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 3)
        models = [car.model for car in response.context["car_list"]]
        self.assertIn("Camry", models)
        self.assertIn("Corolla", models)
        self.assertIn("Civic", models)


class DriverSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

        User.objects.create_user(
            username="driver1",
            password="password1",
            license_number="ABC12345"
        )
        User.objects.create_user(
            username="driver2",
            password="password2",
            license_number="DEF67890"
        )
        User.objects.create_user(
            username="driver3",
            password="password3",
            license_number="GHI13579"
        )

    def setUp(self):
        self.client.login(
            username="testuser",
            password="testpass"
        )

    def test_driver_search_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"driver": "driver1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(
            response.context["driver_list"][0].username, "driver1"
        )

    def test_driver_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"driver": "nonexistent"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 0)

    def test_driver_search_partial_match(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"driver": "driver"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 3)
        usernames = [
            driver.username for driver
            in response.context["driver_list"]
        ]
        self.assertIn("driver1", usernames)
        self.assertIn("driver2", usernames)
        self.assertIn("driver3", usernames)
