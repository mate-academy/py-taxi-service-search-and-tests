from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required_redirect_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            expected_url="/accounts/login/?next=/manufacturers/"
        )


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test",
            password="Test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        Manufacturer.objects.create(
            name="test_name2",
            country="test_country2"
        )
        response = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicDriverTest(TestCase):
    def test_login_require_redirect_driver(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            expected_url="/accounts/login/?next=/drivers/"
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user1",
            "password1": "User1234test1",
            "password2": "User1234test1",
            "first_name": "Test first1",
            "last_name": "Test last1",
            "license_number": "TES12348"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PublicCarTest(TestCase):
    def test_login_require_redirect_car(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            expected_url="/accounts/login/?next=/cars/"
        )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        test_manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        Car.objects.create(
            model="Test",
            manufacturer=test_manufacturer
        )
        Car.objects.create(
            model="Test1",
            manufacturer=test_manufacturer
        )

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
