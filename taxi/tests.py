from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Driver, Car, Manufacturer


class DriverSearchTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create_user(
            username="john",
            password="testpass123",
            license_number="TEST001",
        )
        self.driver2 = Driver.objects.create_user(
            username="johnny",
            password="testpass123",
            license_number="TEST002",
        )
        self.driver3 = Driver.objects.create_user(
            username="maria",
            password="testpass123",
            license_number="TEST003",
        )

    def test_search_by_username(self):
        self.client.force_login(self.driver1)

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver_list"].count(), 2)

    def test_search_by_username_no_results(self):
        self.client.force_login(self.driver1)

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "unknown"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["driver_list"].count(), 0)


class CarSearchTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )

        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )

        self.car3 = Car.objects.create(
            model="BMW X5",
            manufacturer=self.manufacturer,
        )

    def test_search_by_model(self):
        self.client.force_login(
            Driver.objects.create_user(
                username="testdriver",
                password="testpass123",
                license_number="TEST004",
            )
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Cam"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car_list"].count(), 1)
        self.assertEqual(
            response.context["car_list"][0].model,
            "Camry",
        )

    def test_search_by_model_no_results(self):
        self.client.force_login(
            Driver.objects.create_user(
                username="testdriver",
                password="testpass123",
                license_number="TEST005",
            )
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Unknown"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["car_list"].count(), 0)


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

    def test_search_by_name(self):
        driver = Driver.objects.create_user(
            username="testdriver",
            password="testpass123",
            license_number="TEST006",
        )
        self.client.force_login(driver)

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toy"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["manufacturer_list"].count(),
            1,
        )
        self.assertEqual(
            response.context["manufacturer_list"][0].name,
            "Toyota",
        )

    def test_search_by_name_no_results(self):
        driver = Driver.objects.create_user(
            username="testdriver2",
            password="testpass123",
            license_number="TEST007",
        )
        self.client.force_login(driver)

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Unknown"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["manufacturer_list"].count(),
            0,
        )


class DriverModelTest(TestCase):
    def test_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="urltest",
            password="testpass123",
            license_number="TEST008",
        )

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )


class ModelStringTest(TestCase):
    def test_model_str_methods(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        driver = Driver.objects.create_user(
            username="john",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="TEST009",
        )

        car = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(manufacturer), "Toyota Japan")
        self.assertEqual(str(driver), "john (John Doe)")
        self.assertEqual(str(car), "Camry")


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver",
            password="testpass123",
            license_number="TEST010",
        )

        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.car = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer,
        )

    def test_assign_car_to_driver(self):
        self.client.force_login(self.driver)

        response = self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": self.car.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.driver.cars.filter(pk=self.car.pk).exists()
        )

    def test_unassign_car_from_driver(self):
        self.driver.cars.add(self.car)

        self.client.force_login(self.driver)

        response = self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                kwargs={"pk": self.car.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            self.driver.cars.filter(pk=self.car.pk).exists()
        )
