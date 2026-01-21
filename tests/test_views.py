from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicViewTests(TestCase):
    def test_login_required(self) -> None:
        result_index = self.client.get(INDEX_URL)
        result_manuf = self.client.get(MANUFACTURER_LIST_URL)
        result_car = self.client.get(CAR_LIST_URL)
        result_driver = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(result_index.status_code, 200)
        self.assertNotEqual(result_manuf.status_code, 200)
        self.assertNotEqual(result_car.status_code, 200)
        self.assertNotEqual(result_driver.status_code, 200)


class PrivateManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TEST USER",
            password="test12345"
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2",
        )

    def test_retrieve_manufacturer_list(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TEST USER",
            password="test12345"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )

    def test_retrieve_car_list(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test Driver",
            password="Test12345",
            first_name="Test First Name",
            last_name="Test Last Name",
            license_number="ABC54321",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
