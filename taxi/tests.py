from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car, Driver


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="Bob",
            last_name="Smith",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="Bob",
            last_name="Smith",
        )
        car = Car.objects.create(
            model="test_car",
            manufacturer=manufacturer,
        )
        car.drivers.set([driver])
        self.assertEqual(str(car), car.model)


class PublicCarTest(TestCase):

    def setUp(self):
        self.client = Client()

    """Testing car-views for client, who don't login """
    def test_login_required(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    """"Testing for logined client"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        Car.objects.create(model="test", manufacturer=manufacturer)
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(res.context["car_list"]), list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "tesla",
            "first_name": "test123",
            "last_name": "test123",
            "license_number": "BOB09631",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }

        response = self.client.post(reverse("taxi:driver-create"), data=form_data)

        # перевірка, що форма пройшла успішно (редірект)
        self.assertEqual(response.status_code, 302)

        # тепер можна шукати
        new_driver = Driver.objects.get(license_number=form_data["license_number"])
        self.assertEqual(new_driver.username, form_data["username"])

    def test_create_manufacturer(self):
        form_data = {
            "name": "test",
            "country": "test",
        }
        res = self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_man = Manufacturer.objects.get(name=form_data["name"])
        self.assertEqual(new_man.name, form_data["name"])
        self.assertEqual(res.status_code, 302)


class CarCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="admin123", is_staff=True
        )
        self.client.login(username="admin", password="admin123")

        self.manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")

        self.driver1 = Driver.objects.create_user(
            username="driver1", password="testpass1", license_number="AAA111"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2", password="testpass2", license_number="BBB222"
        )

    def test_create_car(self):
        form_data = {
            "model": "Cybertruck",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }

        response = self.client.post(reverse("taxi:car-create"), data=form_data)

        self.assertEqual(response.status_code, 302)  # Очікується редірект після успішного створення

        new_car = Car.objects.get(model="Cybertruck")

        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer, self.manufacturer)
        self.assertQuerysetEqual(
            new_car.drivers.order_by("id"),
            Driver.objects.filter(id__in=[self.driver1.id, self.driver2.id]).order_by("id"),
            transform=lambda x: x
        )


class DriverListViewTest(TestCase):
    def setUp(self):
        self.password = "testpass123"
        self.user = get_user_model().objects.create_user(
            username="admin", password=self.password, is_staff=True
        )
        self.client.login(username="admin", password=self.password)

        Driver.objects.create_user(
            username="john_doe", password="pass1", license_number="ABC12123"
        )
        Driver.objects.create_user(
            username="jane_smith", password="pass2", license_number="XYZ34456"
        )
        Driver.objects.create_user(
            username="alice", password="pass3", license_number="LMN35789"
        )

    def test_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "john"}
        )

        self.assertEqual(response.status_code, 200)

        drivers = response.context["driver_list"]  # or "object_list"
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "john_doe")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "notfound"}
        )

        self.assertEqual(response.status_code, 200)
        drivers = response.context["driver_list"]
        self.assertEqual(len(drivers), 0)


class CarListViewTest(TestCase):
    def setUp(self):
        self.password = "testpass123"
        self.user = get_user_model().objects.create_user(
            username="admin", password=self.password, is_staff=True
        )
        self.client.login(username="admin", password=self.password)

        self.manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )

        Car.objects.create(model="Model S", manufacturer=self.manufacturer)
        Car.objects.create(model="Cybertruck", manufacturer=self.manufacturer)
        Car.objects.create(model="Mustang", manufacturer=self.manufacturer)

    def test_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "model"}
        )

        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]  # або object_list
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Model S")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "somethingunknown"}
        )

        self.assertEqual(response.status_code, 200)
        cars = response.context["car_list"]
        self.assertEqual(len(cars), 0)


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.password = "testpass123"
        self.user = get_user_model().objects.create_user(
            username="admin", password=self.password, is_staff=True
        )
        self.client.login(username="admin", password=self.password)

        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "tes"}
        )

        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]  # або object_list
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "Tesla")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "BMW"}
        )

        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 0)