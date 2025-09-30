from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse

from taxi.forms import CarSearchForm, DriverSearchForm
from taxi.models import Car, Manufacturer


# Create your tests here.
class TestCarSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        self.client.force_login(self.user)

        self.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.audi = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

        self.car = Car.objects.create(
            model="M4",
            manufacturer=self.bmw,
        )
        self.car.drivers.add(self.user)

        self.bmw_m5 = Car.objects.create(
            model="M5",
            manufacturer=self.bmw,
        )
        self.bmw_m5.drivers.add(self.user)

        self.audi_a4 = Car.objects.create(
            model="A4",
            manufacturer=self.audi,
        )
        self.audi_a4.drivers.add(self.user)

        self.url = reverse("taxi:car-list")

    def test_access_to_the_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_shows_all_cars(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_search_form_in_context(self):
        response = self.client.get(self.url)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)

    def test_search_exact_model(self):
        response = self.client.get(self.url, {"model": "M4"})
        cars = response.context["car_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "M4")

    def test_search_few_models(self):
        response = self.client.get(self.url, {"model": "M"}, )
        cars = response.context["car_list"]
        self.assertEqual(len(cars), 2)
        models = [car.model for car in cars]
        self.assertIn("M4", models)
        self.assertIn("M5", models)


class TestDriverSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        self.client.force_login(self.user)
        self.user1 = get_user_model().objects.create_user(
            username="Jake",
            first_name="Test1",
            last_name="User1",
            license_number="ETA12345",
        )
        self.user2 = get_user_model().objects.create_user(
            username="Joan",
            first_name="Test1",
            last_name="User1",
            license_number="ETQ12345",
        )
        self.user3 = get_user_model().objects.create_user(
            username="Garry",
            first_name="Test1",
            last_name="User1",
            license_number="ETS12345",
        )
        self.url = reverse("taxi:driver-list")

    def test_access_to_the_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_check_form(self):
        response = self.client.get(self.url, {"username": ""}, )
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            DriverSearchForm
        )

    def test_show_all_drivers(self):
        response = self.client.get(self.url, {"username": ""}, )
        self.assertEqual(len(response.context["driver_list"]), 4)

    def test_show_all_j_drivers(self):
        response = self.client.get(self.url, {"username": "J"}, )
        cont = response.context["driver_list"]
        self.assertEqual(len(cont), 2)
        drivers = [d.username for d in cont]
        self.assertIn("Joan", drivers)
        self.assertIn("Jake", drivers)

    def test_show_exact_driver(self):
        response = self.client.get(self.url, {"username": "Garry"}, )
        cont = response.context["driver_list"]
        self.assertEqual(len(cont), 1)
        self.assertEqual("Garry", cont[0].username)


class TestManufacturerSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.url = reverse("taxi:manufacturer-list")

    def test_access_to_the_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_search_form_in_context(self):
        response = self.client.get(self.url)
        self.assertIn("search_form", response.context)

    def test_search_all_model(self):
        response = self.client.get(self.url, {"name": ""}, )
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_search_exact_model(self):
        response = self.client.get(self.url, {"name": "BMW"}, )
        self.assertEqual("BMW", response.context["manufacturer_list"][0].name)

    def test_search_few_manufacturers(self):
        response = self.client.get(self.url, {"name": "M"})
        manufacturers = response.context["manufacturer_list"]
        manufacturers1 = [i.name for i in manufacturers]
        self.assertIn("BMW", manufacturers1)
        self.assertIn("Mercedes", manufacturers1)
