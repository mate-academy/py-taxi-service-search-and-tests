from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from taxi.models import Car, Manufacturer, Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", kwargs={"pk": 1})
DRIVER_DELETE_URL = reverse("taxi:driver-delete", kwargs={"pk": 1})

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": 1})
CAR_DELETE_URL = reverse("taxi:car-delete", kwargs={"pk": 1})

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})


class PublicViewsTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create_user(
            username="Test username",
            license_number="TES45678",
            first_name="Test name",
            last_name="Test surname"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test manufacturer name",
            country="Test manufacturer country"
        )
        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="Test car model"
        )
        self.car.drivers.add(self.driver)

        self.client = Client()

    def test_login_required_manufacturer_lit(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_create(self):
        res = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_update(self):
        res = self.client.get(MANUFACTURER_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manufacturer_delete(self):
        res = self.client.get(MANUFACTURER_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_lit(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_detail(self):
        res = self.client.get(CAR_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_create(self):
        res = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_update(self):
        res = self.client.get(CAR_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_delete(self):
        res = self.client.get(CAR_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_drivers_lit(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_detail(self):
        res = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_create(self):
        res = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_update(self):
        res = self.client.get(DRIVER_UPDATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_delete(self):
        res = self.client.get(DRIVER_DELETE_URL)
        self.assertNotEqual(res.status_code, 200)
