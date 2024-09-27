from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
HOME_URL = reverse("taxi:index")


class PublicAccessTest(TestCase):
    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_home_page_login_required(self):
        res = self.client.get(HOME_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateAccessTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        first_manufacturer = Manufacturer.objects.create(
            name="test_manufacturer_1",
            country="test_country_1"
        )

        second_manufacturer = Manufacturer.objects.create(
            name="test_manufacturer_2",
            country="test_country_2"
        )

        Car.objects.create(
            model="test_model_1",
            manufacturer=first_manufacturer
        )

        Car.objects.create(
            model="test_model_2",
            manufacturer=second_manufacturer
        )

    def test_retrive_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search_by_name(self):
        search_parameter = {"name": "test_manufacturer_1"}
        response = self.client.get(MANUFACTURER_URL, search_parameter)
        manufacturers = Manufacturer.objects.filter(
            name__icontains=search_parameter["name"]
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_retrive_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search_by_model(self):
        search_parameter = {"model": "test_model_1"}
        response = self.client.get(CAR_URL, search_parameter)
        cars = Car.objects.filter(
            model__icontains=search_parameter["model"]
        )

        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_retrive_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search_by_username(self):
        Driver.objects.create_user(
            username="test_username_1",
            password="test123",
            license_number="TST12345"
        )
        Driver.objects.create_user(
            username="test_username_2",
            password="test1234",
            license_number="TST54321"
        )

        search_parameter = {"username": "test_username"}
        response = self.client.get(DRIVER_URL, search_parameter)
        drivers = Driver.objects.filter(
            username__icontains=search_parameter["username"]
        )

        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
