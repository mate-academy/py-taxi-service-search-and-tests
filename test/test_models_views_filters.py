from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer, Driver
from django.core.exceptions import ValidationError


class ManufacturerTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_manufacturer_creation(self):
        self.assertEqual(self.manufacturer.name, "Toyota")
        self.assertEqual(self.manufacturer.country, "Japan")

    def test_str_representation(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")


class CarTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")
        self.car = Car.objects.create(model="X5", manufacturer=self.manufacturer)

    def test_car_creation(self):
        self.assertEqual(self.car.model, "X5")
        self.assertEqual(self.car.manufacturer.name, "BMW")

    def test_str_representation(self):
        self.assertEqual(str(self.car), "X5")

    def test_car_has_manufacturer(self):
        self.assertEqual(self.car.manufacturer.name, "BMW")


class DriverTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="12345ABC"
        )

    def test_driver_creation(self):
        driver = Driver.objects.get(username="driver1")
        self.assertEqual(driver.first_name, "John")
        self.assertEqual(driver.last_name, "Doe")
        self.assertEqual(driver.license_number, "12345ABC")

    def test_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), f"/drivers/{self.driver.id}/")


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password123"
        )
        manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
        for i in range(7):
            Car.objects.create(model=f"Model {i}", manufacturer=manufacturer)

    def test_car_list_pagination(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_car_search_filter(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:car-list"), {"model": "Model 1"})
        self.assertContains(response, "Model 1")


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password123"
        )
        for name in ["Audi", "Toyota", "Ford"]:
            Manufacturer.objects.create(name=name, country="Country")

    def test_manufacturer_list_content(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertContains(response, "Audi")
        self.assertContains(response, "Toyota")

    def test_manufacturer_search_filter(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "Toyota"})
        self.assertContains(response, "Toyota")


        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "Ford"})
        self.assertContains(response, "Ford")


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password123"
        )
        for i in range(5):
            Driver.objects.create(
                username=f"driver{i}",
                first_name=f"First{i}",
                last_name=f"Last{i}",
                license_number=f"1234{i}"
            )

    def test_driver_list_pagination(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)


class CarDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password123"
        )
        self.manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")
        self.car = Car.objects.create(model="X5", manufacturer=self.manufacturer)

    def test_car_detail_view(self):
        self.client.login(username="user", password="password123")
        response = self.client.get(reverse("taxi:car-detail", kwargs={"pk": self.car.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")
        self.assertContains(response, "BMW")


class ManufacturerDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="password123"
        )
        self.manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
