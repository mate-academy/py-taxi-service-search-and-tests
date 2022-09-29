from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm, validate_license_number
from taxi.models import Manufacturer


class FormsTest(TestCase):

    def test_driver_creation_form_with_additional_fields(self):
        form_data = {
            "username": "vasa_test",
            "password1": "qwerty12345test",
            "password2": "qwerty12345test",
            "first_name": "vasa_test",
            "last_name": "chak_test",
            "license_number": "ASD33445"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_license_form_with_additional_fields(self):
        license_number = {"license_number": "AYT33445"}

        form = DriverLicenseUpdateForm(data=license_number)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, license_number)

    def test_validate_license_number(self):
        correct_data = "UYT33344"
        wrong_data = {
            "license_number1": "ASD33",
            "license_number2": "Adf33445",
            "license_number3": "ASDdf445",
            "license_number4": "aER33445",
            "license_number5": "AER3344534",
            "license_number6": "AER33445df",
            "license_number7": "AER3344!",
            "license_number8": "{AER33443}",
            }
        for value in wrong_data.values():
            with self.assertRaises(ValidationError):
                validate_license_number(value)

        form1 = validate_license_number(correct_data)
        self.assertEqual(form1, "UYT33344")

    def test_car_creation_form(self):
        manufacturer = Manufacturer.objects.create(
            name="test111",
            country="ua"
        )
        driver1 = get_user_model().objects.create_user(
            username="vasa_test1",
            password="qwerty12345test1",
            first_name="vasa_test1",
            last_name="chak_test1",
            license_number="ASD33459"
        )
        driver2 = get_user_model().objects.create_user(
            username="vasa_test13",
            password="qwerty12345test13",
            first_name="vasa_test13",
            last_name="chak_test13",
            license_number="ASD33455"
        )

        form_data = {
            "model": "test12",
            "manufacturer": manufacturer,
            "drivers": [driver1, driver2]
           }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], form_data["model"])
        self.assertEqual(form.cleaned_data["manufacturer"], form_data["manufacturer"])
