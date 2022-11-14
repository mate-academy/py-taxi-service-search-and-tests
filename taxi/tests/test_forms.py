from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer


class FormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "test.test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "first",
            "last_name": "last",
            "license_number": "TES12345",
        }

    def test_driver_creation_form_with_license_number(self):
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

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

    def test_license_number_validation(self):
        license_numbers = [
            "",
            "A123",
            "DFE1",
            "123456789",
            "DFR123456",
        ]

        for license_number in license_numbers:
            with self.subTest(license_number=license_number):
                self.form_data.update({"license_number": license_number})

                form = DriverCreationForm(data=self.form_data)

                self.assertFalse(form.is_valid())
