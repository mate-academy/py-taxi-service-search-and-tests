from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        Manufacturer.objects.create(
            name="test_name2",
            country="test_country2"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturer_with_parameters(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "test_name1"})
        manufacturer = Manufacturer.objects.filter(name="test_name1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        get_user_model().objects.create_user(
            username="test_user1",
            password="test_password1",
            license_number="test_license_number1"
        )
        get_user_model().objects.create_user(
            username="test_user2",
            password="test_password2",
            license_number="test_license_number2"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 3)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_with_parameters(self):
        response = self.client.get(DRIVER_URL, {"username": "test_user1"})
        driver = get_user_model().objects.filter(username="test_user1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver))
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        Car.objects.create(
            model="test_model1",
            manufacturer=Manufacturer.objects.create(
                name="test_name1",
                country="test_country1"
            )
        )
        Car.objects.create(
            model="test_model2",
            manufacturer=Manufacturer.objects.create(
                name="test_name2",
                country="test_country2"
            )
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_with_parameters(self):
        response = self.client.get(CAR_URL, {"model": "test_model1"})
        car = Car.objects.filter(model="test_model1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car))
        self.assertTemplateUsed(response, "taxi/car_list.html")
