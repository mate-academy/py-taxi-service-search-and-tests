from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Manufacturer, Driver


class CarFormTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        self.driver = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="1test2"
        )

    def test_car_creation_form(self) -> None:
        form_data = {
            "model": "test_model",
            "manufacturer": self.manufacturer,
            "drivers": get_user_model().objects.all()
        }

        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_with_valid_data(self) -> None:
        form_data = {
            "username": "test_username",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "AAA55555",
            "password1": "user12test",
            "password2": "user12test",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_update_license(self) -> None:
        form = DriverLicenseUpdateForm(data={
            "license_number": "AAA12345"
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data,
            {"license_number": "AAA12345"}
        )

