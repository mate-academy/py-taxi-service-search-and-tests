from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

DRIVER_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
HOME = reverse("taxi:index")
LOGIN = reverse("login")


class PublicAccessForbiddenTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_public_access_forbidden_driver_list(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_public_access_forbidden_car_list(self):
        response = self.client.get(CARS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_public_access_forbidden_manufacturer_list(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_public_access_forbidden_home(self):
        response = self.client.get(HOME)

        self.assertNotEqual(response.status_code, 200)

    def test_public_access_granted_login(self):
        response = self.client.get(LOGIN)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class PrivateAccessGrantedTest(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="testcountry"
        )
        Car.objects.create(
            model="testmodel",
            manufacturer=manufacturer
        )

        self.user = get_user_model().objects.create_user(
            "test",
            "pass1223"
        )
        self.client.force_login(self.user)

    def test_private_access_granted_driver_list(self):
        response = self.client.get(DRIVER_URL)

        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_private_access_granted_car_list(self):
        response = self.client.get(CARS_URL)

        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_private_access_granted_manufacturer_list(self):
        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_private_access_granted_home(self):
        response = self.client.get(HOME)

        self.assertEqual(response.status_code, 200)

    def test_private_access_granted_login(self):
        response = self.client.get(LOGIN)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class PrivateCreationTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "testuser",
            "Testpass123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "qweqweqwe",
            "password1": "asdasda123",
            "password2": "asdasda123",
            "first_name": "jack test",
            "last_name": "black test",
            "license_number": "JAK12312",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
