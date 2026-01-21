from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_DETAILS_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
DRIVER_DETAILS_URL = reverse("taxi:driver-detail", kwargs={"pk": 2})


class PublicTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_car_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_user_can_see_car_list(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        Car.objects.create(
            manufacturer=manufacturer,
            model="Test Model",
        )
        Car.objects.create(
            manufacturer=manufacturer,
            model="Test Model 2",
        )
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(res.context["car_list"]), list(cars))

    def test_user_can_see_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(res.status_code, 200)

    def test_user_can_see_driver_list(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(res.status_code, 200)

    def test_user_can_see_car_details(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        car = Car.objects.create(
            manufacturer=manufacturer,
            model="Test Model",
        )
        res = self.client.get(CAR_DETAILS_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["car"], car)

    def test_user_can_see_driver_details(self):
        driver = Driver.objects.create(
            username="Test Driver",
            first_name="Test First",
            last_name="Test Last",
            password="<PASSWORD>",
            license_number="ABC12345",
        )
        res = self.client.get(DRIVER_DETAILS_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["driver"], driver)
