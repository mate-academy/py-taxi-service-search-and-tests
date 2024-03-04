from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-create")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="username.test",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_retrieve_user_manufacturer(self):
        Manufacturer.objects.create(
            name="Manufacturer-first",
            country="Country-first"
        )
        Manufacturer.objects.create(
            name="Manufacturer-last",
            country="Country-last"
        )
        response = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturer)
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
            "username.test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_create_car(self):
        model_car_first = "model-first"
        model_car_last = "model-last"
        manufacturer_first = Manufacturer.objects.create(
            name="name-first", country="Country-first"
        )
        manufacturer_last = Manufacturer.objects.create(
            name="name-last", country="Country-last"
        )
        driver = get_user_model().objects.create_user(
            username="driver.test",
            password="password123",
            license_number="ABC09876"
        )
        car_first = Car.objects.create(
            model=model_car_first, manufacturer=manufacturer_first
        )
        car_first.drivers.add(driver)
        car_last = Car.objects.create(
            model=model_car_last, manufacturer=manufacturer_last
        )
        car_last.drivers.add(driver)

        car_all = Car.objects.all()
        self.assertEqual(car_all.count(), 2)
        self.assertEqual(
            Car.objects.get(
                model=model_car_first).manufacturer,
            manufacturer_first
        )
        self.assertEqual(
            Car.objects.get(
                model=model_car_last).manufacturer,
            manufacturer_last
        )


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "username.test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "user",
            "password1": "Password_123",
            "password2": "Password_123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "TES45678",
        }

        self.client.post(DRIVER_URL, data=form_data)
        user_test = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(user_test.first_name, form_data["first_name"])
        self.assertEqual(user_test.last_name, form_data["last_name"])
        self.assertEqual(user_test.license_number, form_data["license_number"])
