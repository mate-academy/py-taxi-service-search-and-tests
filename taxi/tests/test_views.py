from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTets(TestCase):

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "test12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="VAZ", country="Germany")

        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )


class ToggleAssignToCarTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver = get_user_model().objects.create_user(
            username="user",
            password="user12345",
            license_number="SWE12345"
        )
        self.car = Car.objects.create(
            model="RAV4",
            manufacturer=self.manufacturer
        )
        self.url = reverse(
            "taxi:toggle-car-assign",
            args=[self.car.id]
        )

    def test_toggle_assign_to_car(self):
        self.client.force_login(self.driver)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.car in self.driver.cars.all())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.car not in self.driver.cars.all())
