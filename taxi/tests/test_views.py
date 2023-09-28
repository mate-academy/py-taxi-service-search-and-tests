from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse

from taxi.models import Driver, Manufacturer

INDEX_URL = reverse_lazy("taxi:index")
MANUFACTURERS_URL = reverse_lazy("taxi:manufacturer-list")
DRIVERS_URL = reverse_lazy("taxi:driver-list")
CARS_URL = reverse_lazy("taxi:car-list")


class PublicTests(TestCase):
    def test_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_login_required_manufacturer_list(self) -> None:
        res = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_driver_list(self) -> None:
        res = self.client.get(DRIVERS_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_list(self) -> None:
        res = self.client.get(CARS_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_driver", "password123"
        )

        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="driver1_test", license_number="TTI12345"
        )
        Driver.objects.create(
            username="driver2_test", license_number="TTG12345"
        )

        response = self.client.get(DRIVERS_URL)

        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

        self.assertTemplateUsed("taxi:driver-list")

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "license_number": "TTT12345",
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "passwordtest",
            "password2": "passwordtest",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "testusername", "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Renault", country="France")
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed("taxi:manufacturer-list")

    def test_create_manufacturer(self):
        form_data = {"name": "Renault", "country": "France"}
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)

        manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(manufacturer.country, form_data["country"])
