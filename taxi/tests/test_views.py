from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="best",
            country="best_country",
        )
        Manufacturer.objects.create(
            name="worse",
            country="worse_country",
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        Manufacturer.objects.create(
            name="best",
            country="best_country",
        )
        Manufacturer.objects.create(
            name="worse",
            country="worse_country",
        )
        response = self.client.get(MANUFACTURER_URL, {"name": "best"})
        object_list = response.context["manufacturer_list"]
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].name, "best")
        self.assertContains(response, "best")
        self.assertNotContains(response, "worse")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Driver.objects.create(
            username="test_1",
            license_number="ABC12345",
            password="test12345",
        )
        Driver.objects.create(
            username="test_2",
            license_number="ABC12346",
            password="test12345",
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver(self):
        Driver.objects.create(
            username="test_1",
            license_number="ABC12345",
            password="test12345",
        )
        Driver.objects.create(
            username="test_2",
            license_number="ABC12346",
            password="test12345",
        )
        response = self.client.get(DRIVER_URL, {"username": "test_1"})
        object_list = response.context["driver_list"]
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].username, "test_1")
        self.assertContains(response, "test_1")
        self.assertNotContains(response, "test_2")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Lastivka",
            country="Ukraine",
        )
        driver = Driver.objects.create(
            username="test_1",
            license_number="ABC12345",
            password="test12345",
        )
        car_toyota = Car.objects.create(
            model="Toyota",
            manufacturer=manufacturer,
        )
        car_bmw = Car.objects.create(
            model="BMW",
            manufacturer=manufacturer,
        )
        car_toyota.drivers.add(driver)
        car_bmw.drivers.add(driver)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Lastivka",
            country="Ukraine",
        )
        driver = Driver.objects.create(
            username="test_1",
            license_number="ABC12345",
            password="test12345",
        )
        car_toyota = Car.objects.create(
            model="Toyota",
            manufacturer=manufacturer,
        )
        car_bmw = Car.objects.create(
            model="BMW",
            manufacturer=manufacturer,
        )
        car_toyota.drivers.add(driver)
        car_bmw.drivers.add(driver)
        response = self.client.get(CAR_URL, {"model": "Toyota"})
        object_list = response.context["car_list"]
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].model, "Toyota")
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")
