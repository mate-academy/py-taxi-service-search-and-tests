from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car, Manufacturer

User = get_user_model()


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john",
            password="pass12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "john (John Doe)")


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "Camry")


class DriverCRUDTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john",
            password="pass12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.client.login(username="john", password="pass12345")

    def test_driver_list(self):
        self.client.get(reverse("taxi:driver-list"))

    def test_driver_create(self):
        self.client.post(
            reverse("taxi:driver-create"),
            {
                "username": "mike",
                "password1": "pass12345",
                "password2": "pass12345",
                "license_number": "DEF67890",
                "first_name": "Mike",
                "last_name": "Smith",
            },
        )
        self.assertEqual(Driver.objects.filter(username="mike").count(), 1)


class ManufacturerCRUDTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="john",
            password="pass12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.client.login(username="john", password="pass12345")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_manufacturer_list(self):
        self.client.get(reverse("taxi:manufacturer-list"))

    def test_manufacturer_create(self):
        self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Honda", "country": "Japan"},
        )
        self.assertEqual(Manufacturer.objects.filter(name="Honda").count(), 1)


class CarCRUDTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="john",
            password="pass12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.client.login(username="john", password="pass12345")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

    def test_car_list(self):
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        self.client.get(reverse("taxi:car-list"))

    def test_car_create(self):
        self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Camry",
                "manufacturer": self.manufacturer.id,
                "drivers": [],
            },
        )
        self.assertEqual(Car.objects.filter(model="Camry").count(), 1)

    def test_car_update(self):
        car = Car.objects.create(model="OldModel",
                                 manufacturer=self.manufacturer
                                 )
        self.client.post(
            reverse("taxi:car-update", args=[car.id]),
            {
                "model": "NewModel",
                "manufacturer": self.manufacturer.id,
                "drivers": [],
            },
        )
        car.refresh_from_db()
        self.assertEqual(car.model, "NewModel")


# ----------------------------
# SEARCH TESTS
# ----------------------------
class DriverSearchTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create_user(
            username="alice",
            password="pass12345",
            license_number="AAA11111",
        )
        self.driver2 = Driver.objects.create_user(
            username="bob",
            password="pass12345",
            license_number="BBB22222",
        )
        self.client.login(username="alice", password="pass12345")

    def test_search_no_query_returns_all(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(len(response.context["driver_list"]), 2)

    def test_search_partial_match(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"query": "ali"}
                                   )
        self.assertIn(self.driver1, response.context["driver_list"])
        self.assertNotIn(self.driver2, response.context["driver_list"])

    def test_search_case_insensitive(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"query": "ALICE"}
                                   )
        self.assertIn(self.driver1, response.context["driver_list"])


class CarSearchTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car1 = Car.objects.create(model="Camry",
                                       manufacturer=self.manufacturer
                                       )
        self.car2 = Car.objects.create(model="Corolla",
                                       manufacturer=self.manufacturer
                                       )
        self.user = Driver.objects.create_user(
            username="alice",
            password="pass12345",
            license_number="AAA11111",
        )
        self.client.login(username="alice", password="pass12345")

    def test_search_no_query_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(len(response.context["car_list"]), 2)

    def test_search_partial_match(self):
        response = self.client.get(reverse("taxi:car-list"), {"query": "Cam"})
        self.assertIn(self.car1, response.context["car_list"])
        self.assertNotIn(self.car2, response.context["car_list"])

    def test_search_case_insensitive(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"query": "camry"}
                                   )
        self.assertIn(self.car1, response.context["car_list"])


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.m1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.m2 = Manufacturer.objects.create(name="Honda", country="Japan")
        self.user = Driver.objects.create_user(
            username="alice",
            password="pass12345",
            license_number="AAA11111",
        )
        self.client.login(username="alice", password="pass12345")

    def test_search_no_query_returns_all(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_search_partial_match(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"query": "Toy"}
                                   )
        self.assertIn(self.m1, response.context["manufacturer_list"])
        self.assertNotIn(self.m2, response.context["manufacturer_list"])

    def test_search_case_insensitive(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"query": "TOYOTA"}
                                   )
        self.assertIn(self.m1, response.context["manufacturer_list"])
