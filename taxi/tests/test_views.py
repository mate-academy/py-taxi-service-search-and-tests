from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicCarListViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarListViewTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer_name",
            country="test_manufacturer_country",
        )
        self.car_x = Car.objects.create(
            model="test_model_X",
            manufacturer=self.manufacturer,
        )
        self.car_y = Car.objects.create(
            model="test_model_Y",
            manufacturer=self.manufacturer,
        )
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_cars(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "x"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_model_X")
        self.assertNotContains(response, "test_model_Y")


class PublicManufacturerListViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListViewTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer_x = Manufacturer.objects.create(
            name="test_manufacturer_name_x",
            country="test_manufacturer_country_x",
        )
        self.manufacturer_y = Manufacturer.objects.create(
            name="test_manufacturer_name_y",
            country="test_manufacturer_country_y",
        )
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturers(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "x"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_manufacturer_name_x")
        self.assertNotContains(response, "test_manufacturer_name_y")


class PublicDriverListViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user_x = get_user_model().objects.create_user(
            username="test_username_x",
            password="1qazcde3",
            license_number="XXX12345",
        )
        self.user_y = get_user_model().objects.create_user(
            username="test_username_y",
            password="1qazcde3",
            license_number="YYY12345",
        )
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "admin",
            "password1": "1qazxsw2F45",
            "password2": "1qazxsw2F45",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "RRR12645",
        }
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=form_data,
        )
        self.assertEqual(response.status_code, 302)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"],
        )

    def test_search_drivers(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "x"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_username_x")
        self.assertNotContains(response, "test_username_y")
