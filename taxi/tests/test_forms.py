from django.test import TestCase

from django.contrib.auth import get_user_model

from taxi.forms import DriverCreationForm, CarForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer


class FormTests(TestCase):

    def setUp(self) -> None:

        self.manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )

        self.driver = get_user_model().objects.create(
            username="user",
            first_name="John",
            last_name="Black",
            email="johnblack@gmail.com",
            license_number="ASD12344"
        )

    def test_car_form_widget_type(self):

        form_data = {
            "model": "Eclipse",
            "manufacturer": self.manufacturer,
            "drivers": self.driver,
        }

        form = CarForm(data=form_data)

        self.assertEqual(
            form.fields["drivers"].widget.__class__.__name__,
            "CheckboxSelectMultiple")

    def test_driver_creation_form_with_license_first_last_names(self):

        form_data = {
            "username": "testuser",
            "license_number": "ASD12345",
            "first_name": "John",
            "last_name": "Black",
            "password1": "testuserpassword12",
            "password2": "testuserpassword12",
        }

        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_incorrect_license_length(self):
        form_data = {
            "username": "testuser",
            "license_number": "ASSD123456",
            "password1": "testuserpassword12",
            "password2": "testuserpassword12",
        }

        form_incorrect_length = DriverCreationForm(
            data=form_data
        )
        self.assertFalse(form_incorrect_length.is_valid())

    def test_driver_creation_form_with_incorrect_license_upper_letters(self):
        form_data = {
            "username": "testuser",
            "license_number": "AsD12345",
            "password1": "testuserpassword12",
            "password2": "testuserpassword12",
        }

        form_incorrect_upper_letters = DriverCreationForm(
            data=form_data
        )
        self.assertFalse(form_incorrect_upper_letters.is_valid())

    def test_driver_creation_form_with_incorrect_license_quant_digits(self):
        form_data = {
            "username": "testuser",
            "license_number": "ASDS1234",
            "password1": "testuserpassword12",
            "password2": "testuserpassword12",
        }

        form_incorrect_quant_digits = DriverCreationForm(
            data=form_data
        )
        self.assertFalse(form_incorrect_quant_digits.is_valid())

    def test_driver_update_license_form(self):

        form_data = {
            "license_number": "SSD12345"
        }

        form = DriverLicenseUpdateForm(
            data=form_data, instance=self.driver
        )

        self.assertTrue(form.is_valid())
        case = form.save()
        self.assertEqual(case.license_number, form_data["license_number"])
