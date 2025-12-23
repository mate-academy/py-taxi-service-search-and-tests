from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create()
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})")


class PublicManufacturerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test_username",
            password="test_123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        manufacturer_url = reverse("taxi:manufacturer-list")
        Manufacturer.objects.create(name="test_name1")
        Manufacturer.objects.create(name="test_name2")
        response = self.client.get(manufacturer_url)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))


class PublicCarTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test_username",
            password="test_123",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        car_url = reverse("taxi:car-list")
        manufacturer = Manufacturer.objects.create()
        Car.objects.create(model="test_model1", manufacturer=manufacturer)
        Car.objects.create(model="test_model2", manufacturer=manufacturer)
        response = self.client.get(car_url)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))


class PublicDriverTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test_username",
            password="test_123",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        driver_url = reverse("taxi:driver-list")
        Driver.objects.create(username="Bob", license_number="TYU12345")
        Driver.objects.create(username="Alice", license_number="ASD54321")
        response = self.client.get(driver_url)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_create_driver(self):
        form_data = {
            "username": "BobFontain",
            "password1": "test_123",
            "password2": "test_123",
            "first_name": "Bob",
            "last_name": "Fontain",
            "license_number": "XCV12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"])

        self.assertEqual(new_driver.username, form_data["username"])
        self.assertEqual(new_driver.license_number,
                         form_data["license_number"])
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])


class ManufacturerSearchViewTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="Mercedes-Benz")
        Manufacturer.objects.create(name="Volkswagen")
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_manufacturer_list(self):
        manufacturer_url = reverse("taxi:manufacturer-list")
        response = self.client.get(
            manufacturer_url,
            data={"name": "Merc"},
        )
        self.assertEqual(response.status_code, 200)
        queryset = response.context["manufacturer_list"]
        returned_manufacturers = {
            manufacturer.name for manufacturer in queryset
        }
        self.assertEqual(returned_manufacturers, {"Mercedes-Benz"})
        self.assertEqual(response.status_code, 200)


class CarSearchViewTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create()
        Car.objects.create(model="Passat",
                           manufacturer=manufacturer)
        Car.objects.create(model="AMG",
                           manufacturer=manufacturer)
        self.user = get_user_model().objects.create_user(
            username="user",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_cars_search(self):
        car_url = reverse("taxi:car-list")
        response = self.client.get(
            car_url,
            data={"model": "pas"},
        )
        self.assertEqual(response.status_code, 200)
        queryset = response.context["car_list"]
        returned_models = {car.model for car in queryset}
        self.assertEqual(returned_models, {"Passat"})
        self.assertEqual(response.status_code, 200)


class DriverSearchViewTest(TestCase):
    def setUp(self):
        Driver.objects.create(username="Jeremy",
                              license_number="HJK123456")
        Driver.objects.create(username="bob",
                              license_number="ASD456123")
        self.user = get_user_model().objects.create(
            username="test_username",
            password="test_123",
        )
        self.client.force_login(self.user)

    def test_search_drivers(self):
        driver_url = reverse("taxi:driver-list")
        response = self.client.get(
            driver_url,
            data={"username": "Jere"},
        )
        queryset = response.context["driver_list"]
        returned_usernames = {driver.username for driver in queryset}
        self.assertEqual(returned_usernames, {"Jeremy"})
        self.assertEqual(response.status_code, 200)
