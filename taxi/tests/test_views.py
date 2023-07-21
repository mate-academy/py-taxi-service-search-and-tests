from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(country="Germany")

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Test Manufacturer")
        searched_name = "Test"
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": searched_name}
        )
        self.assertEqual(response.status_code, 200)
        manufacturer_in_context = Manufacturer.objects.filter(name__icontains=searched_name)
        self.assertQuerysetEqual(response.context["manufacturer_list"], manufacturer_in_context)


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEquals(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123",
            "ABC12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(name="BMW")
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_manufacturer_by_name(self):
        manufacturer = Manufacturer.objects.create(name="BMW")
        Car.objects.create(model="M5", manufacturer=manufacturer)
        searched_model = "M"
        response = self.client.get(
            CAR_URL,
            {"model": searched_model}
        )
        self.assertEqual(response.status_code, 200)
        car_in_context = Car.objects.filter(model__icontains=searched_model)
        self.assertQuerysetEqual(response.context["car_list"], car_in_context)


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEquals(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver(self):
        Driver.objects.create(username="Test")
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_manufacturer_by_name(self):
        Driver.objects.create(username="TestDriver")
        searched_username = "Test"
        response = self.client.get(
            DRIVER_URL,
            {"username": searched_username}
        )
        self.assertEqual(response.status_code, 200)
        driver_in_context = Driver.objects.filter(username__icontains=searched_username)
        self.assertQuerysetEqual(response.context["driver_list"], driver_in_context, ordered=False)
