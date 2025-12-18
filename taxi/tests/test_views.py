from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver

HOME_URL = reverse("taxi:index")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicPagesTest(TestCase):
    def test_home_login_required(self):
        res = self.client.get(HOME_URL)
        self.assertRedirects(res, "/accounts/login/?next=" + HOME_URL)

    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertRedirects(res, "/accounts/login/?next=" + MANUFACTURER_URL)

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertRedirects(res, "/accounts/login/?next=" + CAR_URL)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertRedirects(res, "/accounts/login/?next=" + DRIVER_URL)


class PrivatePagesTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)


class IndexViewTest(PrivatePagesTest):
    def test_index_counts_and_visits(self):
        Manufacturer.objects.create(name="BMW")
        Driver.objects.create_user(
            username="driver1",
            password="pass12345",
            license_number="ABC12345"
        )

        response = self.client.get(HOME_URL)

        self.assertEqual(response.status_code, 200)
        self.assertIn("num_visits", response.context)
        self.assertEqual(response.context["num_visits"], 1)


class ManufacturerListViewTest(PrivatePagesTest):
    def setUp(self):
        super().setUp()
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Audi")

    def test_search_by_name(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "BMW"})
        manufacturers = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "BMW")


class CarListViewTest(PrivatePagesTest):
    def setUp(self):
        super().setUp()
        manufacturer = Manufacturer.objects.create(name="Tesla")
        Car.objects.create(model="Model S", manufacturer=manufacturer)
        Car.objects.create(model="Model X", manufacturer=manufacturer)

    def test_search_by_model(self):
        response = self.client.get(CAR_URL, {"model": "Model S"})
        cars = response.context["car_list"]

        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Model S")


class DriverListViewTest(PrivatePagesTest):
    def setUp(self):
        super().setUp()
        Driver.objects.create_user(
            username="john_doe",
            password="pass12345",
            license_number="ABC12345"
        )
        Driver.objects.create_user(
            username="alice",
            password="pass12345",
            license_number="DEF67890"
        )

    def test_search_by_username(self):
        response = self.client.get(DRIVER_URL, {"username": "john"})
        drivers = response.context["driver_list"]

        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "john_doe")


class ToggleAssignToCarViewTest(PrivatePagesTest):
    def setUp(self):
        super().setUp()
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="pass12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

        self.manufacturer = Manufacturer.objects.create(name="Ford")
        self.car = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer
        )

    def test_assign_driver_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        self.client.get(url)

        self.assertIn(self.car, self.driver.cars.all())

    def test_remove_driver_from_car(self):
        self.driver.cars.add(self.car)

        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        self.client.get(url)

        self.assertNotIn(self.car, self.driver.cars.all())
