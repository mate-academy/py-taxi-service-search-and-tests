from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car

DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            "Den",
            "Driver123"
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver(self):
        Driver.objects.create(
            username="John",
            password="12345",
            license_number="LOM58412"
        )
        Driver.objects.create(
            username="Lina",
            password="123456",
            license_number="GOI90875"
        )
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.filter(username__icontains="n")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver(self):
        Driver.objects.create(
            username="Test",
            password="1876545",
            license_number="LOM54572"
        )
        Driver.objects.create(
            username="Test2",
            password="987654325",
            license_number="GOI76545"
        )
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.filter(username__icontains="e")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        for driver in response.context["driver_list"]:
            self.assertIn("e", driver.username)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            "David",
            "David9999"
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="Mercedes-benz",
            country="German"
        )
        Manufacturer.objects.create(
            name="Audi",
            country="German"
        )
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.filter(name__icontains="d")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        Manufacturer.objects.create(
            name="Cadillac",
            country="USA"
        )
        Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.filter(name__icontains="l")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            "Stepan",
            "asdf43eewqd3Q"
        )
        self.client.force_login(self.driver)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Mercedes",
            country="German"
        )
        Car.objects.create(
            model="Mercedes-benz",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="BMW",
            manufacturer=manufacturer
        )
        response = self.client.get(CAR_URL)
        cars = Car.objects.filter(model__icontains="M")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Renault",
            country="French"
        )
        Car.objects.create(
            model="Vauxhall",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Nissan",
            manufacturer=manufacturer
        )
        response = self.client.get(CAR_URL)
        cars = Car.objects.filter(model__icontains="a")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
