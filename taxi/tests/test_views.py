from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

INDEX_URL = reverse("taxi:index")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_DELETE_URL = "taxi:manufacturer-delete"
CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = "taxi:car-detail"
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_DELETE_URL = "taxi:car-delete"
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = "taxi:driver-detail"
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_DELETE_URL = "taxi:driver-delete"


class UserWithoutLoginTest(TestCase):
    def test_index_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_list_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_list_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_list_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class LoggedInUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password",
            license_number="EFG98765"
        )
        self.client.force_login(self.user)

    def test_index_success(self):
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Cars:")
        self.assertContains(res, "Drivers:")
        self.assertContains(res, "Manufacturers")
        self.assertContains(res, "You have visited this page")

    def test_view_create_driver(self):
        username = "Test_Username"
        password = "test_password"
        license_number = "ABC12345"
        data = {
            "username": username,
            "password": password,
            "license_number": license_number
        }
        response = self.client.post(DRIVER_CREATE_URL, data)
        self.assertEqual(response.status_code, 200)

    def test_view_display_driver(self):
        res = self.client.get(reverse(DRIVER_DETAIL_URL, kwargs={"pk": self.user.id}))
        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.license_number)

    def test_delete_driver_get_request(self):
        res = self.client.get(reverse(DRIVER_DELETE_URL, kwargs={"pk": self.user.id}))
        self.assertContains(res, "Delete driver?")

    def test_view_create_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer"
        )
        model = "Test_car"
        data = {
            "model": model,
            "manufacturer": manufacturer,
            "drivers": (self.user, )
        }
        response = self.client.post(CAR_CREATE_URL, data)
        self.assertEqual(response.status_code, 200)

    def test_view_display_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer"
        )
        model = "Test_car"
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )
        car.drivers.set((self.user, ))
        res = self.client.get(reverse(CAR_DETAIL_URL, kwargs={"pk": car.id}))
        self.assertContains(res, self.user.username)
        self.assertContains(res, manufacturer.name)
        self.assertContains(res, model)

    def test_delete_car_get_request(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer"
        )
        model = "Test_car"
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )
        res = self.client.get(reverse(CAR_DELETE_URL, kwargs={"pk": car.id}))
        self.assertContains(res, "Delete car?")

    def test_view_delete_car(self):
        cars_before = Car.objects.count()
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer"
        )
        model = "Test_car"
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )
        res = self.client.post(reverse(CAR_DELETE_URL, kwargs={"pk": car.id}))
        cars_after = Car.objects.count()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(cars_before, cars_after)

    def test_view_create_manufacturer(self):
        name = "test_manufacturer"
        data = {
            "name": name
        }
        response = self.client.post(MANUFACTURER_CREATE_URL, data)
        self.assertEqual(response.status_code, 200)

    def test_delete_manufacturer_get_request(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer"
        )
        res = self.client.get(reverse(MANUFACTURER_DELETE_URL, kwargs={"pk": manufacturer.id}))
        self.assertContains(res, "Delete manufacturer?")

    def test_view_delete_manufacturer(self):
        manufacturer_before = Manufacturer.objects.count()
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer"
        )
        res = self.client.post(reverse(MANUFACTURER_DELETE_URL, kwargs={"pk": manufacturer.id}))
        manufacturer_after = Manufacturer.objects.count()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(manufacturer_before, manufacturer_after)
