from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "JIM31313"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "JIM31313"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_update_driver_license(self):
        new_user = get_user_model().objects.create_user(
            username="new_user",
            password="user12test",
            first_name="Test first",
            last_name="Test last",
            license_number="JIM31313"
        )
        form_data = {
            "license_number": "JIM31314"
        }
        self.client.post(reverse(
            "taxi:driver-update",
            args=[new_user.id]),
            data=form_data
        )
        updated_user = get_user_model().objects.get(id=new_user.id)

        self.assertEqual(
            updated_user.license_number,
            form_data["license_number"]
        )


class DriverSearchFormTest(TestCase):
    def test_form_is_valid_with_valid_username(self):
        form_data = {
            "username": "user",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_form_is_valid(self):
        form_data = {
            "model": "Super",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Super")


class ManufacturerSearchFormTest(TestCase):
    def test_form_is_valid(self):
        form_data = {
            "name": "Manufacturer",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Manufacturer")
