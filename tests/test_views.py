# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taxi_service.settings")
#
# import django
# django.setup()
#

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

# user
USERNAME = "Zina"
PASSWORD = "ZinaForsage69"

# urls:
CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicManufacturerTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        Manufacturer.objects.create(
            name="Bogdan",
            country="Ukraine"
        )
        Manufacturer.objects.create(
            name="Bober",
            country="Poland"
        )
        self.user = get_user_model().objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self) -> None:
        response = self.client.get(MANUFACTURERS_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_search(self) -> None:
        response = self.client.get(MANUFACTURERS_URL, {"name": "Bober"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__in=["Bogdan", "Bober"]),
        )


class PublicCarTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        Manufacturer.objects.create(
            name="FG33",
            country="China",
        )
        Manufacturer.objects.create(
            name="LKD",
            country="Taiwan",
        )
        Car.objects.create(
            model="666",
            manufacturer=Manufacturer.objects.get(id=1)
        )
        Car.objects.create(
            model="777",
            manufacturer=Manufacturer.objects.get(id=2)
        )
        Car.objects.get(id=1).drivers.add(self.user)
        Car.objects.get(id=2).drivers.add(self.user)
        self.client.force_login(self.user)

    def test_retrieve_car_list(self) -> None:
        response = self.client.get(CARS_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_search(self) -> None:
        response = self.client.get(CARS_URL, {"model": "666"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(
                model="666"
            )
            )
        )


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )
        self.client.force_login(self.user)

    def test_create_driver(self) -> None:
        form_data = {
            "username": USERNAME + "_",
            "password1": PASSWORD + "_",
            "password2": PASSWORD + "_",
            "first_name": "John",
            "last_name": "Pedro",
            "license_number": "AHK12345",
        }
        self.client.post(
            reverse("taxi:driver-create"), data=form_data
        )
        new_user = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_user.first_name, form_data["first_name"]
        )
        self.assertEqual(
            new_user.last_name, form_data["last_name"]
        )
        self.assertEqual(
            new_user.license_number, form_data["license_number"]
        )
