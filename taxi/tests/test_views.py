from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class SearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="admin",
            password="test12345",
            license_number="ADM12345",
        )

        self.client.force_login(self.user)

        self.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.corolla = Car.objects.create(
            model="Corolla",
            manufacturer=self.toyota,
        )

        self.camry = Car.objects.create(
            model="Camry",
            manufacturer=self.toyota,
        )

        self.driver_john = Driver.objects.create_user(
            username="john_driver",
            password="test12345",
            license_number="JOH12345",
        )

        self.driver_alex = Driver.objects.create_user(
            username="alex_driver",
            password="test12345",
            license_number="ALE12345",
        )

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toy"},
        )

        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]

        self.assertIn(self.toyota, manufacturers)
        self.assertNotIn(self.bmw, manufacturers)

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "cor"},
        )

        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]

        self.assertIn(self.corolla, cars)
        self.assertNotIn(self.camry, cars)

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )

        self.assertEqual(response.status_code, 200)

        drivers = response.context["driver_list"]

        self.assertIn(self.driver_john, drivers)
        self.assertNotIn(self.driver_alex, drivers)

    def test_empty_driver_search_returns_all_drivers(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": ""},
        )

        drivers = response.context["driver_list"]

        self.assertIn(self.driver_john, drivers)
        self.assertIn(self.driver_alex, drivers)


class ToggleAssignToCarTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john",
            password="test12345",
            license_number="ABC12345",
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )

        self.client.force_login(self.driver)

    def test_assign_driver_to_car(self):
        self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": self.car.pk},
            )
        )

        self.assertIn(
            self.driver,
            self.car.drivers.all(),
        )

    def test_remove_driver_from_car(self):
        self.car.drivers.add(self.driver)

        self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": self.car.pk},
            )
        )

        self.assertNotIn(
            self.driver,
            self.car.drivers.all(),
        )


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="test_user",
            password="test12345",
            license_number="TES12345",
        )

        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )

    def test_index_contains_correct_counts(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["num_drivers"],
            1,
        )
        self.assertEqual(
            response.context["num_cars"],
            1,
        )
        self.assertEqual(
            response.context["num_manufacturers"],
            1,
        )

    def test_index_increases_num_visits(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(
            response.context["num_visits"],
            1,
        )

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(
            response.context["num_visits"],
            2,
        )
