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
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        Manufacturer.objects.create(
            name="test_name2",
            country="test_country2"
        )
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
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
        response = self.client.get(DRIVER_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
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
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")
