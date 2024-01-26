from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer
from taxi.forms import (
    DriversSearchForm,
    CarsSearchForm,
    ManufacturersSearchForm
)

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicLiteraryFormatTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        driver = self.client.get(DRIVER_URL)
        car = self.client.get(CAR_URL)
        manufacturer = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(driver.status_code, 200)
        self.assertNotEqual(car.status_code, 200)
        self.assertNotEqual(manufacturer.status_code, 200)


class PrivateLiteraryFormatTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="Bmw")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateAuthorTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="user", password="test12test"
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_search_driver_by_username(self):
        Driver.objects.create(username="user1", license_number="ABC12345")
        Driver.objects.create(username="user2", license_number="ABC54321")

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "user2"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            DriversSearchForm
        )
        self.assertQuerysetEqual(
            response.context["object_list"],
            Driver.objects.filter(username__icontains="user2"),
        )

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="testmanufacturer")
        driver = get_user_model().objects.create(
            username="test user",
            password="Test12test",
            first_name="test_firstname",
            last_name="test_lastname",
            license_number="TST12312",
        )
        car1 = Car.objects.create(model="car1", manufacturer=manufacturer)
        car2 = Car.objects.create(model="car2", manufacturer=manufacturer)
        car1.drivers.set([driver])
        car2.drivers.set([driver])

        response = self.client.get(
            reverse("taxi:car-list"), {"model": "car1"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], CarsSearchForm)
        self.assertQuerysetEqual(
            response.context["object_list"],
            Car.objects.filter(model__icontains="car1"),
        )
