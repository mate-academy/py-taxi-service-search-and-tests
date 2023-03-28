from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Car, Manufacturer


class FormTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "testuser",
            "password1": "testpass1",
            "password2": "testpass1",
            "first_name": "test",
            "last_name": "testovich",
            "license_number": "ASdqw1253453",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivetDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="testpass1234"
        )
        self.client.force_login(self.user)

    def test_driver_creation(self):
        form_data = {
            "username": "testu",
            "password1": "testpass4345",
            "password2": "testpass4345",
            "first_name": "testik",
            "last_name": "testovich",
            "license_number": "ASdfdsf12343",
        }
        self.client.post(
            path=reverse("taxi:driver-create"),
            data=form_data
        )
        new_user = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class SearchFormTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_name",
            password="testpass1412344",
            license_number="ASdfdfsf1245"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.user)

    def test_manufacturer_search_form(self):
        search_term = {"name": "BMW"}
        response = self.client.get(
            path=reverse("taxi:manufacturer-list"),
            data=search_term
        )

        self.assertContains(response, search_term["name"])

    def test_driver_search_form(self):
        search_term = {"username": "test_name"}
        response = self.client.get(
            path=reverse("taxi:driver-list"),
            data=search_term
        )

        self.assertContains(response, search_term["username"])

    def test_car_search_form(self):
        search_term = {"model": "BMW"}
        response = self.client.get(
            path=reverse("taxi:car-list"),
            data=search_term
        )

        self.assertContains(response, search_term["model"])
