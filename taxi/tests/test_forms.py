from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarModelSearchForm,
    ManufacturerNameSearchForm,
    DriverLicenseUpdateForm,
    DriverUsernameSearchForm,
    DriverCreationForm
)
from taxi.models import Manufacturer


class TestCarForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="top_user",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )

    def test_car_search_form_with_arg(self):
        form_data = {
            "model": "M5",
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_search_form_without_arg(self):
        form_data = {
            "model": "",
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestManufacturerForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="top_user",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )

    def test_manufacturer_search_form_with_arg(self):
        form_data = {
            "name": "BMW",
        }
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_without_arg(self):
        form_data = {
            "name": "",
        }
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestDriverForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="top_user",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )

    def test_driver_form(self):
        form_data = {
            "username": "new_user",
            "license_number": "VFX12345",
            "password1": "Qwerty12345!",
            "password2": "Qwerty12345!"
        }
        form = DriverCreationForm(form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_with_arg(self):
        form_data = {
            "username": "user1",
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_search_form_without_arg(self):
        form_data = {
            "username": "",
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_license_form_correct_num(self):
        form_data = {"license_number": "VFX12345"}
        form = DriverLicenseUpdateForm(form_data)
        self.assertTrue(form.is_valid())

    def test_update_license_form_incorrect_num(self):
        form_data = {"license_number": "Vx1245"}
        form = DriverLicenseUpdateForm(form_data)
        self.assertEqual(form.is_valid(), False)
