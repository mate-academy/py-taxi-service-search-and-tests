from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTests(TestCase):

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTests(TestCase):

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Lada")
        Manufacturer.objects.create(name="Daewoo")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        lada = Manufacturer.objects.create(name="Lada")
        daewoo = Manufacturer.objects.create(name="Daewoo")
        Car.objects.create(model="Lanos", manufacturer=daewoo)
        Car.objects.create(model="Niva", manufacturer=lada)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        get_user_model().objects.create_user(
            username="testuser1",
            password="test1233",
            license_number="TES12345"
        )
        get_user_model().objects.create_user(
            username="testuser2",
            password="test1244",
            license_number="TES12346"
        )
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "license_number": "TES12345",
            "first_name": "Test_name",
            "last_name": "Test_last_name",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_driver.first_name,
            form_data["first_name"]
        )
        self.assertEqual(
            new_driver.last_name,
            form_data["last_name"]
        )
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
