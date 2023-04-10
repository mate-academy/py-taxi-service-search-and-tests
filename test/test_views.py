from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

DRIVER_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
HOME = reverse("taxi:index")
LOGIN = reverse("login")


class PublicAccessForbiddenTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_public_access_forbidden_driver(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_public_access_forbidden_car(self):
        response = self.client.get(CARS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_public_access_forbidden_manufacturer(self):
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
            country="country_test"
        )
        Car.objects.create(
            model="model_test",
            manufacturer=manufacturer
        )

        self.user = get_user_model().objects.create_user(
            "test",
            "edcujm37"
        )
        self.client.force_login(self.user)

    def test_private_access_granted_driver(self):
        response = self.client.get(DRIVER_URL)

        drivers = get_user_model().objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_private_access_granted_car(self):
        response = self.client.get(CARS_URL)

        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_private_access_granted_manufacturer(self):
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

    def test_search_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=te"
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            Driver.objects.filter(username__icontains="te")
        )
