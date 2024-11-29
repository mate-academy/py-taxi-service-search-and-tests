from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, CarForm
from taxi.models import Manufacturer, Car, Driver


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class FormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="bmw",
            country="germany"
        )
        self.driver_data = {
            "username": "test_new_user",
            "password1": "test_password1",
            "password2": "test_password1",
            "license_number": "ABC12345",
            "first_name": "test_first_test",
            "last_name": "test_last_test",
        }
        self.manufacturer_data = {
            "name": "bmw",
            "country": "germany"
        }
        self.car_data = {
            "model": "x5",
            "manufacturer": self.manufacturer,
            "drivers": [self.user]
        }
        self.client.force_login(self.user)

    def test_driver_creation_form_with_license_number_is_valid(self):
        form = DriverCreationForm(data=self.driver_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.driver_data)

    def test_create_driver(self):
        self.client.post(reverse("taxi:driver-create"), data=self.driver_data)
        new_user = get_user_model().objects.get(
            username=self.driver_data["username"]
        )

        self.assertEqual(new_user.first_name, self.driver_data["first_name"])
        self.assertEqual(new_user.last_name, self.driver_data["last_name"])
        self.assertEqual(
            new_user.license_number,
            self.driver_data["license_number"]
        )

    def test_car_creation_form(self):
        form = CarForm(data=self.car_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["model"],
            self.car_data["model"]
        )
        self.assertEqual(
            form.cleaned_data["manufacturer"],
            self.car_data["manufacturer"]
        )

    def test_create_manufacturer(self):
        self.client.post(
            reverse("taxi:manufacturer-create"),
            data=self.manufacturer_data
        )
        new_manufacturer = Manufacturer.objects.get(
            name=self.manufacturer_data["name"]
        )

        self.assertEqual(
            new_manufacturer.name,
            self.manufacturer_data["name"]
        )
        self.assertEqual(
            new_manufacturer.country,
            self.manufacturer_data["country"]
        )

    def test_create_manufacture_with_invalid_data(self):
        data = {
            "name": "zaz",
        }
        res = self.client.post(
            reverse("taxi:manufacturer-create"),
            data=data
        )
        self.assertNotEqual(res.status_code, 201)

    def test_create_car_with_invalid_data(self):
        data = {
            "model": "x5",
            "manufacturer": self.manufacturer
        }

        res = self.client.post(
            reverse("taxi:car-create"),
            data=data
        )

        self.assertNotEqual(res.status_code, 201)

    def test_create_driver_with_invalid_data(self):
        data = {
            "username": "test_username1234",
            "password1": "test1234",
            "password2": "test1234"
        }

        res = self.client.post(
            reverse("taxi:driver-create"),
            data=data
        )

        self.assertNotEqual(res.status_code, 201)

    def test_search_car_with_invalid_data(self):
        Car.objects.create(
            model="X5",
            manufacturer=Manufacturer.objects.create(
                name="BMW",
                country="Germany"
            )
        )
        Car.objects.create(
            model="S-Class",
            manufacturer=Manufacturer.objects.create(
                name="Mercedes",
                country="Germany"
            )
        )
        res = self.client.get(f"{CAR_URL}?model=wrg2ff")
        self.assertEqual(list(res.context["car_list"]), [])

    def test_search_driver_with_invalid_data(self):
        Driver.objects.create_user(
            username="test1user",
            password="test1user",
            license_number="ABC12345"
        )
        Driver.objects.create_user(
            username="test2user",
            password="test2user",
            license_number="DEF67890"
        )
        res = self.client.get(f"{DRIVER_URL}?username=invalidtest")
        self.assertEqual(list(res.context["driver_list"]), [])

    def test_search_manufacturer_with_invalid_data(self):
        Manufacturer.objects.create(
            name="Alfa Romeo",
            country="Italy"
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        res = self.client.get(f"{MANUFACTURER_URL}?name=zaz")
        self.assertEqual(list(res.context["manufacturer_list"]), [])
