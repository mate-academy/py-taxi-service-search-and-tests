from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class TestManufacturerForm(TestCase):
    def setUp(self) -> None:
        self.superuser = get_user_model().objects.create_superuser(
            username="superuser",
            password="password",
            first_name="first_name",
            last_name="last_name",
            license_number="license_number",
        )

        self.client = Client()
        self.client.force_login(self.superuser)

    def test_create_manufacturer(self):
        form_data = {
            "name": "Porsche",
            "country": "Germany",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])


class TestCarForm(TestCase):
    def setUp(self) -> None:
        self.superuser = get_user_model().objects.create_superuser(
            username="superuser",
            password="password",
            first_name="first_name",
            last_name="last_name",
            license_number="license_number",
        )

        self.client = Client()
        self.client.force_login(self.superuser)

    def test_create_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Porsche", country="Germany"
        )
        form_data = {
            "model": "911",
            "manufacturer": manufacturer.id,
            "drivers": [self.superuser.id],
        }

        self.client.post(reverse("taxi:car-create"), data=form_data)

        new_car = Car.objects.get(model=form_data["model"])

        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer, manufacturer)
        self.assertEqual(list(new_car.drivers.all()), [self.superuser])


class TestDriverForm(TestCase):
    def setUp(self) -> None:
        self.superuser = get_user_model().objects.create_superuser(
            username="superuser",
            password="password",
            first_name="first_name",
            last_name="last_name",
            license_number="license_number",
        )

        self.client = Client()
        self.client.force_login(self.superuser)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "first_name": "first_name",
            "last_name": "last_name",
            "password1": "qwtyasd103krjr!jrt",
            "password2": "qwtyasd103krjr!jrt",
            "license_number": "ABC12345",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)

        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.username, form_data["username"])
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertTrue(new_driver.check_password(form_data["password1"]))
        self.assertEqual(
            new_driver.license_number, form_data["license_number"]
        )
