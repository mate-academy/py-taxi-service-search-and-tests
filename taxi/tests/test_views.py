from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="Mercedes")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class ManufacturerSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="Mercedes")
        Manufacturer.objects.create(name="Toyota")

    def test_search_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "Audi"})

        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.filter(name__icontains="Audi")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )

        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_no_search_query(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(name="Toyota")

    def test_retrieve_cars(self):
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)

        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(name="Toyota")

        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)

    def test_search_car(self):
        response = self.client.get(CAR_URL, {"model": "Corolla"})
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.filter(model__icontains="Corolla")

        self.assertEqual(len(response.context["car_list"]), cars.count())

    def test_no_search_query(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_create_drivers(self):
        Driver.objects.create(username="driver1", license_number="12345")
        Driver.objects.create(username="driver2", license_number="54321")

        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class DriverSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        Driver.objects.create(username="driver1", license_number="11111")
        Driver.objects.create(username="driver2", license_number="22222")
        Driver.objects.create(username="driver3", license_number="33333")

    def test_search_driver(self):
        response = self.client.get(DRIVER_URL, {"username": "driver1"})

        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.filter(username__icontains="driver1")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_no_search_query(self):
        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
