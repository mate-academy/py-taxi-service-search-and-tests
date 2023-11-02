from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-create")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_user",
            "test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="test_name_first",
            country="test_country_first"
        )
        Manufacturer.objects.create(
            name="test_name_second",
            country="test_country_second"
        )
        Manufacturer.objects.create(
            name="test_name_third",
            country="test_country_third"
        )

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


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_user",
            "test12345"
        )
        self.client.force_login(self.user)

    def test_create_car(self):
        model_first = "model_test_first"
        model_second = "model_test_second"
        manufacturer_first = Manufacturer.objects.create(
            name="name_test_first",
            country="county_test_first"
        )
        manufacturer_second = Manufacturer.objects.create(
            name="name_test_second",
            country="county_test_second"
        )
        driver = get_user_model().objects.create_user(
            username="user_test",
            password="test12345",
            license_number="ABC98765"
        )
        car_test_first = Car.objects.create(
            model=model_first,
            manufacturer=manufacturer_first
        )
        car_test_first.drivers.add(driver)

        car_test_second = Car.objects.create(
            model=model_second,
            manufacturer=manufacturer_second
        )
        car_test_second.drivers.add(driver)

        car_test_all = Car.objects.all()

        self.assertEqual(car_test_all.count(), 2)
        self.assertEqual(
            Car.objects.get(model=model_first).manufacturer,
            manufacturer_first
        )
        self.assertEqual(
            Car.objects.get(model=model_second).manufacturer,
            manufacturer_second
        )


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_user",
            "test12345"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "user_test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "ABC98765"
        }

        self.client.post(DRIVER_URL, data=form_data)
        user_test = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(user_test.first_name, form_data["first_name"])
        self.assertEqual(user_test.last_name, form_data["last_name"])
        self.assertEqual(user_test.license_number, form_data["license_number"])
