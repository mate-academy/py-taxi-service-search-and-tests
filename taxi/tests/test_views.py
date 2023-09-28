from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class UnauthorisedAccessTest(TestCase):
    def test_manufacturer_anonymous_user_access_denied(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_car_anonymous_user_access_denied(self) -> None:
        response = self.client.get(CAR_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_driver_anonymous_user_access_denied(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertNotEquals(response.status_code, 200)


class AuthorisedAccessTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="ABC12345",
            password="strongPassword"
        )
        self.test_manufacturer = Manufacturer.objects.create(
            name="Test manufacturer", country="Undefined"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_search(self) -> None:
        manufacturer_list = [
            ("BMW", "Germany"),
            ("Toyota", "Japan"),
            ("Lincoln", "Usa")
        ]

        for name, country in manufacturer_list:
            Manufacturer.objects.create(name=name, country=country)

        response = self.client.get(MANUFACTURER_URL, {"name": "o"})

        expected = Manufacturer.objects.filter(name__icontains='o')

        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            expected
        )

    def test_car_list_search(self) -> None:
        car_list = [
            "Toyota Yaris",
            "Mitsubishi Eclipse",
            "Mitsubishi Lancer"
        ]

        for model in car_list:
            Car.objects.create(model=model, manufacturer=self.test_manufacturer)

        response = self.client.get(CAR_URL, {"model": "Mitsubishi"})

        expected = Car.objects.filter(model__icontains='Mitsubishi')

        self.assertQuerysetEqual(
            response.context["car_list"],
            expected,
            ordered=False
        )

    def test_driver_list_search(self) -> None:
        drivers_list = [
            ("admin.user", "ABC00001"),
            ("joyce.byers", "ABC00002"),
            ("jim.hopper", "ABC00003",),
            ("jonathan.byers", "ABC00004",),
            ("dustin.henderson", "ABC00005")
        ]

        for username, license_number in drivers_list:
            get_user_model().objects.create_user(
                username=username,
                first_name="first_name",
                last_name="last_name",
                license_number=license_number,
                password="strong_password"
            )

        response = self.client.get(DRIVER_URL, {"username": "j"})

        expected = Driver.objects.filter(username__icontains='j')

        self.assertQuerysetEqual(
            response.context["driver_list"],
            expected,
            ordered=False
        )
