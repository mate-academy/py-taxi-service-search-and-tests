from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class LoginRequiredTest(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="AFB34554",
        )
        self.car = Car.objects.create(
            model="M3",
            manufacturer=self.manufacturer
        )
        self.driver.cars.add(self.car)
        self.client.force_login(self.driver)

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        name = self.manufacturer.name
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, name)
        self.assertNotContains(response, "test2")

    def test_retrieve_car(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        car = Car.objects.all()
        self.assertEquals(
            list(response.context["car_list"]),
            list(car),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car(self):
        model = self.car.model
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": model})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, model)
        self.assertNotContains(response, "test2")

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        driver = Driver.objects.all()
        self.assertEquals(
            list(response.context["driver_list"]),
            list(driver),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver(self):
        username = self.driver.username
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": username})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, username)
        self.assertNotContains(response, "test2")
