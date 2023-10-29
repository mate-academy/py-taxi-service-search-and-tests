from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testing123"
        )
        self.client.force_login(self.user)

    def test_get_manufacturers(self):
        Manufacturer.objects.create(
            name="Test manufacturer",
            country="France",
        )
        Manufacturer.objects.create(
            name="Test manufacturer2",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="Test manufacturer3",
            country="Poland",
        )
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test123124",
            password="14uhd1d1d",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "user1",
            "password1": "12376gsda",
            "password2": "12376gsda",
            "first_name": "Testing name",
            "last_name": "Testing last",
            "license_number": "ACD12345",
        }
        self.client.post(reverse("taxi:driver-create"), form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEquals(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="testing123"
        )
        self.client.force_login(self.user)

    def test_get_cars(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test manufacturer1",
            country="France",
        )

        self.manufacturer2 = Manufacturer.objects.create(
            name="Test manufacturer2",
            country="France",
        )

        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="tester12",
            license_number="ADF09876"
        )

        self.car1 = Car.objects.create(
            model="Test car",
            manufacturer=self.manufacturer1,
        )

        self.car1.drivers.add(self.driver1)

        self.car2 = Car.objects.create(
            model="Test car2",
            manufacturer=self.manufacturer2,
        )

        self.car2.drivers.add(self.driver1)

        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
