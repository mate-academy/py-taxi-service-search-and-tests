from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")
DRIVER_FORMAT_URL = reverse("taxi:driver-list")
CAR_FORMAT_URL = reverse("taxi:car-list")


class PublicManufacturerViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(res.status_code, 302)


class PrivateManufacturerViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_list_for_logged_in_user(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(res.status_code, 200)


class PublicCarViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_FORMAT_URL)
        self.assertEqual(res.status_code, 302)


class PrivateCarViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test2",
            password="test1232",
        )
        self.client.force_login(self.user)

    def test_list_for_logged_in_user(self):
        res = self.client.get(CAR_FORMAT_URL)
        self.assertEqual(res.status_code, 200)


class PublicDriverViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_FORMAT_URL)
        self.assertEqual(res.status_code, 302)  # редирект на логін


class PrivateDriverViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test3",
            password="test1233",
        )
        self.client.force_login(self.user)

    def test_list_for_logged_in_user(self):
        res = self.client.get(DRIVER_FORMAT_URL)
        self.assertEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "testuser2",
            "password1": "SecurePass123",
            "password2": "SecurePass123",
            "first_name": "test_first2",
            "last_name": "test_last2",
            "license_number": "ABC11111",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class SearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="test123",
            license_number="ABC11111"
        )

    def test_search_drivers_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.driver, response.context["driver_list"]
        )

    def test_search_cars_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Camry"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.car, response.context["car_list"]
        )

    def test_search_manufacturers_by_name(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list") + "?name=Toyota"
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertIn(
            self.manufacturer, response.context["manufacturer_list"]
        )
