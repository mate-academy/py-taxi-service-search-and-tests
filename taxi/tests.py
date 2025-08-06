from django.test import TestCase
from django.urls import reverse
from .models import Manufacturer, Car, Driver
from django.contrib.auth import get_user_model


User = get_user_model()


class ManufacturerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="moderator",
                                            password="moderator")
        Manufacturer.objects.create(name="Toyota", country="Polska")
        Manufacturer.objects.create(name="Ford", country="Polska")
        Manufacturer.objects.create(name="Tesla", country="Polska")

    def setUp(self):
        self.client.login(username="moderator", password="moderator")

    def test_no_filter_returns_all(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_filter_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": "To"})
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "Toyota")


class CarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="moderator",
                                            password="moderator")

        manufacturer = Manufacturer.objects.create(name="Toyota",
                                                   country="Japan")
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="Camry", manufacturer=manufacturer)
        Car.objects.create(model="Yaris", manufacturer=manufacturer)

    def setUp(self):
        # Logujemy użytkownika przed każdym testem
        self.client.login(username="moderator", password="moderator")

    def test_no_filter_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_filter_by_model_name(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "Co"})
        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Corolla")


class DriverListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="moderator",
            password="moderator",
            license_number="MOD123"
        )
        User.objects.create_user(username="driver1",
                                 password="pass",
                                 license_number="DR123")
        User.objects.create_user(username="driver2",
                                 password="pass",
                                 license_number="DR124")
        User.objects.create_user(username="adminuser",
                                 password="pass",
                                 license_number="DR125")

    def setUp(self):
        self.client.login(username="moderator",
                          password="moderator")

    def test_no_filter_returns_all(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 4)

    def test_filter_by_username(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "driver"})
        self.assertEqual(response.status_code, 200)

        drivers = response.context["driver_list"]
        self.assertEqual(len(drivers), 2)
        self.assertTrue(all("driver" in driver.username
                            for driver in drivers))


class DriverModelTests(TestCase):
    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="testdriver",
            first_name="Jan",
            last_name="Kowalski",
            password="pass",
            license_number="XYZ123"
        )
        self.assertEqual(str(driver), "testdriver (Jan Kowalski)")

    def test_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="testdriver",
            password="pass",
            license_number="XYZ123"
        )
        url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), url)


class CarDriverRelationshipTest(TestCase):
    def test_car_driver_relationship(self):
        manufacturer = Manufacturer.objects.create(name="TestCar",
                                                   country="PL")
        car = Car.objects.create(model="X123", manufacturer=manufacturer)
        driver = User.objects.create_user(username="d1",
                                          password="pass",
                                          license_number="123ABC")

        car.drivers.add(driver)

        self.assertIn(driver, car.drivers.all())
        self.assertIn(car, driver.cars.all())


class DriverPaginationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.moderator = User.objects.create_user(username="moderator",
                                                 password="moderator")
        for i in range(10):
            User.objects.create_user(
                username=f"driver{i}",
                password="pass",
                license_number=f"DR{i:03}"
            )

    def test_pagination_is_five(self):
        self.client.login(username="moderator", password="moderator")

        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("is_paginated", response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)
