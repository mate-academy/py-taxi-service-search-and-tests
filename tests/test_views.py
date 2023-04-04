from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_access_manufacturers(self):
        Manufacturer.objects.create(name="ABC", country="DIDO")
        Manufacturer.objects.create(name="CBA", country="ODID")

        res = self.client.get(MANUFACTURER_LIST_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )

        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test1",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "ABC12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        user_created = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(user_created.first_name,
                         form_data["first_name"])
        self.assertEqual(user_created.license_number,
                         form_data["license_number"])
        self.assertEqual(user_created.last_name,
                         form_data["last_name"])


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_access_cars(self):
        manufacturer = Manufacturer.objects.create(name="ABC", country="DIDO")
        Car.objects.create(model="BMZ", manufacturer=manufacturer)

        res = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")
