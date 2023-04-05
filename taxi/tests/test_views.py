from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_public_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Testusername", password="testpass123456"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Test Manufacturer")
        Manufacturer.objects.create(name="Test Manufacturer 2")

        response = self.client.get(MANUFACTURER_URL)

        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response.context)

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="Ford", country="United States")
        response = self.client.get(MANUFACTURER_URL + "?name=ford")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTest(TestCase):
    def test_public_car(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123456"
        )
        self.client.force_login(self.user)

    def test_private_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="United States"
        )
        Car.objects.create(model="Test1", manufacturer=manufacturer)
        Car.objects.create(model="Test2", manufacturer=manufacturer)

        response = self.client.get(CAR_URL)

        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
        self.assertTemplateUsed(response.context)

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="United States"
        )
        Car.objects.create(model="Ford", manufacturer=manufacturer)
        response = self.client.get(CAR_URL + "?model=ford")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def test_public_manufacturer(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Testusername", password="testpass123456"
        )
        self.client.force_login(self.user)

    def test_private_driver(self):
        Driver.objects.create(
            username="testusername1",
            password="testpass123456",
            license_number="TTT12345",
            first_name="firstname1",
            last_name="lastname1",
        )
        Driver.objects.create(
            username="testusername2",
            password="testpass123456",
            license_number="WWW12345",
            first_name="firstname2",
            last_name="lastname2",
        )

        response = self.client.get(DRIVER_URL)

        driver = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver)
        )
        self.assertTemplateUsed(response.context)

    def test_driver_search(self):
        Driver.objects.create(
            username="testusername",
            password="testpass123456",
            license_number="WWW12345",
            first_name="firstname",
            last_name="lastname",
        )
        response = self.client.get(DRIVER_URL + "?username=testusername")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
