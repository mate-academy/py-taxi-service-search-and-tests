from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="asd12345QW",
            license_number="ASD12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(name="Gord", country="GSA")
        Car.objects.create(model="Pokus", manufacturer=manufacturer)
        Car.objects.create(model="Gokus", manufacturer=manufacturer)
        Car.objects.create(model="Vokus", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )


class SearchViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ASD1234"
        )

        cls.driver1 = get_user_model().objects.create_user(
            username="JohnDriver",
            password="testpass123",
            license_number="AWD1234"
        )
        cls.driver2 = get_user_model().objects.create_user(
            username="MichaelDriver",
            password="testpass123",
            license_number="AqD1234"
        )
        cls.driver3 = get_user_model().objects.create_user(
            username="Alice",
            password="testpass123",
            license_number="AED1234"
        )

        cls.manufacturer1 = Manufacturer.objects.create(
            name="Toyota"
        )
        cls.manufacturer2 = Manufacturer.objects.create(
            name="Mercedes-Benz"
        )
        cls.manufacturer3 = Manufacturer.objects.create(
            name="BMW"
        )

        cls.car1 = Car.objects.create(
            model="Camry",
            manufacturer=cls.manufacturer1,
        )
        cls.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=cls.manufacturer1,
        )
        cls.car3 = Car.objects.create(
            model="Sprinter",
            manufacturer=cls.manufacturer2,
        )

    def setUp(self):
        self.client.login(
            username="testuser",
            password="testpass123",
        )

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )
        self.assertEqual(response.status_code, 200)
        drivers = response.context["driver_list"]
        self.assertEqual(drivers.count(), 1)
        self.assertEqual(drivers[0], self.driver1)

    def test_driver_search_by_part_of_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver"},
        )
        drivers = response.context["driver_list"]
        self.assertEqual(drivers.count(), 2)
        self.assertIn(self.driver1, drivers)
        self.assertIn(self.driver2, drivers)

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "cam"},
        )
        self.assertEqual(response.status_code, 200)
        cars = response.context["car_list"]
        self.assertEqual(cars.count(), 1)
        self.assertEqual(cars[0], self.car1)

    def test_car_search_by_part_of_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "ro"},
        )
        cars = response.context["car_list"]
        self.assertEqual(cars.count(), 1)
        self.assertEqual(cars[0], self.car2)

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"},
        )
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(manufacturers.count(), 1)
        self.assertEqual(
            manufacturers.first(),
            self.manufacturer1,
        )

    def test_manufacturer_search_by_part_of_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "benz"},
        )
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(manufacturers.count(), 1)
        self.assertEqual(
            manufacturers.first(),
            self.manufacturer2,
        )

    def test_driver_list_without_search(self):
        response = self.client.get(
            reverse("taxi:driver-list")
        )
        drivers = response.context["driver_list"]
        self.assertEqual(
            drivers.count(),
            get_user_model().objects.count(),
        )

    def test_car_list_without_search(self):
        response = self.client.get(
            reverse("taxi:car-list")
        )
        cars = response.context["car_list"]
        self.assertEqual(cars.count(), 3)
