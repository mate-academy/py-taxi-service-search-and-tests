from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


MANUFACTURERS_LIST = [
    {
        "name": "Volkswagen",
        "country": "Germany",
    },
    {
        "name": "Fiat",
        "country": "Italy",
    },
    {
        "name": "Volvo",
        "country": "Sweden",
    },
]


def make_a_custom_manufacturers_objects() -> None:
    for manufacturer in MANUFACTURERS_LIST:
        Manufacturer.objects.create(**manufacturer)


class PublicTestManufacturers(TestCase):
    def setUp(self):
        self.client = Client()

    def test_manufacturers_page_for_unlogged_user(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestManufacturers(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="Test1111",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_manufacturers_page_for_logged_user(self):
        for manufacturer in MANUFACTURERS_LIST:
            Manufacturer.objects.create(**manufacturer)

        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(manufacturers),
            list(response.context["manufacturer_list"]),
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html",
        )


class PublicTestDrivers(TestCase):
    def setUp(self):
        self.client = Client()

    def test_drivers_page_for_unlogged_user(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestDrivers(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="Test1111",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_drivers_page_for_logged_in_user(self):
        drivers = [
            {
                "username": "test_driver_1",
                "password": "Test1111",
                "first_name": "Test",
                "last_name": "One",
                "license_number": "ABC11111",
            },
            {
                "username": "test_driver_2",
                "password": "Test22222",
                "first_name": "Test",
                "last_name": "Two",
                "license_number": "ABC22222",
            },
            {
                "username": "test_driver_3",
                "password": "Test33333",
                "first_name": "Test",
                "last_name": "Three",
                "license_number": "ABC33333",
            },
        ]
        for driver in drivers:
            Driver.objects.create(**driver)
        response = self.client.get(DRIVERS_URL)
        self.assertEqual(response.status_code, 200)
        drivers_list = Driver.objects.all()
        response_drivers = response.context["driver_list"]
        for response_driver in response_drivers:
            self.assertIn(
                response_driver,
                list(drivers_list),
            )
        search_username = "2"
        filter_drivers = Driver.objects.filter(
            username__icontains=search_username
        )
        response = self.client.get(
            DRIVERS_URL,
            {
                "username": search_username
            }
        )
        self.assertEqual(
            list(filter_drivers),
            list(response.context["driver_list"]),
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )
        self.assertEqual(
            response.context["search_form"].initial["username"],
            search_username,
        )


class PublicTestCars(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cars_page_for_unlogged_user(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestCars(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="User123!"
        )
        self.client.force_login(self.user)

    def test_cars_page_for_logged_in_user(self):
        make_a_custom_manufacturers_objects()
        manufacturers = {
            manufacturer.name:
                manufacturer for manufacturer in Manufacturer.objects.all()
        }
        cars = [
            {
                "model": "Golf IV",
                "manufacturer": manufacturers["Volkswagen"],
            },
            {
                "model": "Punto",
                "manufacturer": manufacturers["Fiat"],
            },
            {
                "model": "GV35",
                "manufacturer": manufacturers["Volvo"],
            },
        ]
        for car in cars:
            Car.objects.create(**car)
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        car_list = Car.objects.all()
        res_cars = response.context["car_list"]
        for res_car in res_cars:
            self.assertIn(
                res_car,
                list(car_list),
            )
        search_model = "GV35"
        filtered_cars = Car.objects.filter(model__icontains=search_model)
        response = self.client.get(CARS_URL, {"model": search_model})
        self.assertEqual(
            list(filtered_cars),
            list(response.context["car_list"]),
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )
        self.assertEqual(
            response.context["search_form"].initial["model"],
            search_model,
        )
