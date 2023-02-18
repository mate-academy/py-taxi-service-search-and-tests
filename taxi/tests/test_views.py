from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car

DRIVERS_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVERS_URL)

        self.assertNotEqual(res.status_code, 200)
        self.assertRedirects(
            res, expected_url="/accounts/login/?next=/drivers/"
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password"
        )

        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVERS_URL)

        drivers = Driver.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )

    def test_create_driver(self):
        form_data = {
            "username": "username_test",
            "password1": "user_password_test",
            "password2": "user_password_test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "QWE12345"
        }

        self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)
        self.assertRedirects(
            res, expected_url="/accounts/login/?next=/manufacturers/"
        )


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        res = self.client.get(MANUFACTURER_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)
        self.assertRedirects(
            res, expected_url="/accounts/login/?next=/cars/"
        )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        Car.objects.create(
            model="Model S",
            manufacturer=manufacturer
        )
        res = self.client.get(CAR_URL)

        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
