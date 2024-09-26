from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

INDEX_URL = reverse("taxi:index")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicIndexTests(TestCase):

    def test_login_required(self):
        response = self.client.get(INDEX_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateIndexTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_name",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_index(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)


class PublicManufacturerTests(TestCase):

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_name",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Lincoln", country="USA")
        Manufacturer.objects.create(name="Toyota", country="Japan")

        response = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )


class PublicCarTests(TestCase):

    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_name",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer_one = Manufacturer.objects.create(
            name="Lincoln",
            country="USA"
        )
        manufacturer_two = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(
            model="Lincoln Continental",
            manufacturer=manufacturer_one
        )
        Car.objects.create(
            model="Toyota Yaris",
            manufacturer=manufacturer_two
        )

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )


class PublicDriverTests(TestCase):

    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_name",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create(
            username="DriverOne",
            password="driver111",
            license_number="DRV11111"
        )
        get_user_model().objects.create(
            username="DriverTwo",
            password="driver222",
            license_number="DRV22222"
        )
        get_user_model().objects.create(
            username="DriverThree",
            password="driver333",
            license_number="DRV33333"
        )

        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "NWU12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
