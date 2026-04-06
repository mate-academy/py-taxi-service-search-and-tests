from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car, Manufacturer

User = get_user_model()


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="12345"
        )

    def test_login_required(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)

    def test_logged_in_access(self):
        self.client.login(username="test", password="12345")
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "num_drivers",
            response.context
        )
        self.assertIn(
            "num_cars",
            response.context
        )
        self.assertIn(
            "num_manufacturers",
            response.context
        )


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="12345"
        )

        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

    def test_login_required(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        self.assertNotEqual(
            response.status_code,
            200
        )

    def test_filter_by_name(self):
        self.client.login(
            username="test",
            password="12345"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "BMW"}
        )

        self.assertEqual(len(
            response.context["manufacturer_list"]),
            1
        )
        self.assertEqual(
            response.context["manufacturer_list"][0].name,
            "BMW"
        )


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="12345"
        )

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="A6",
            manufacturer=manufacturer
        )

        self.john = Driver.objects.create_user(
            username="john123",
            password="12345",
            license_number="ABC12345"
        )
        self.mike = Driver.objects.create_user(
            username="mike",
            password="12345",
            license_number="XYZ67890"
        )

    def test_login_required(self):
        response = self.client.get(
            reverse("taxi:car-list")
        )
        self.assertNotEqual(
            response.status_code,
            200)

    def test_filter_by_model(self):
        self.client.login(
            username="test",
            password="12345"
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "X5"}
        )

        self.assertEqual(len(
            response.context["object_list"]),
            1
        )


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="12345"
        )

        Driver.objects.create_user(
            username="john123",
            password="12345",
            license_number="ABC12345"
        )

        Driver.objects.create_user(
            username="mike",
            password="12345",
            license_number="XYZ67890"
        )

    def test_login_required(self):
        response = self.client.get(reverse(
            "taxi:driver-list")
        )
        self.assertNotEqual(
            response.status_code,
            200
        )

    def test_filter_by_username(self):
        self.client.login(
            username="test",
            password="12345"
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "john"}
        )

        self.assertEqual(len(
            response.context["object_list"]),
            1
        )


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver",
            password="12345",
            license_number="ABC12345"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )

    def test_add_car_to_driver(self):
        self.client.login(
            username="driver",
            password="12345"
        )

        self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                args=[self.car.id])
        )

        self.driver.refresh_from_db()
        self.assertIn(self.car, self.driver.cars.all())

    def test_remove_car_from_driver(self):
        self.driver.cars.add(self.car)

        self.client.login(
            username="driver",
            password="12345"
        )

        self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                args=[self.car.id])
        )

        self.driver.refresh_from_db()
        self.assertNotIn(self.car, self.driver.cars.all())
