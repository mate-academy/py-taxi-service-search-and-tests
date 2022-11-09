from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer


class FormTest(TestCase):
    def test_driver_creation_form_with_license_number(self):
        form_data = {
            "username": "test.test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first",
            "last_name": "last",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_form(self):
        form_data = {"license_number": "TES12345"}
        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_creation_form(self):
        driver = get_user_model().objects.create_superuser(
            username="test.test",
            password="password12345",
            first_name="first",
            last_name="last",
            license_number="TES12345",
        )
        manufacturer = Manufacturer.objects.create(
            name="test", country="test_country"
        )
        form_data = {
            "model": "model",
            "manufacturer": manufacturer.id,
            "drivers": driver.id,
        }
        url = reverse("taxi:car-create")
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 302)


class ValidateLicenseNumberFormTest(TestCase):
    @staticmethod
    def form_data(license_number: str):
        return DriverLicenseUpdateForm(data={"license_number": license_number})

    def test_license_number_is_valid(self):
        self.assertTrue(self.form_data("TES12345").is_valid())

    def test_should_consist_of_8_characters(self):
        self.assertFalse(self.form_data("").is_valid())
        self.assertFalse(self.form_data("123").is_valid())
        self.assertFalse(self.form_data("123456789").is_valid())
        self.assertFalse(self.form_data("ERT1234").is_valid())
        self.assertFalse(self.form_data("QWe123").is_valid())

    def test_first_3_characters_should_be_uppercase(self):
        self.assertFalse(self.form_data("t!s12345").is_valid())
        self.assertFalse(self.form_data("Tes12345").is_valid())
        self.assertFalse(self.form_data("TeS12345").is_valid())
        self.assertFalse(self.form_data("TT012345").is_valid())

    def test_last_5_characters_should_be_digits(self):
        self.assertFalse(self.form_data("ASDF2345").is_valid())
        self.assertFalse(self.form_data("ASD123#5").is_valid())
