from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        DriverSearchForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        DriverLicenseUpdateForm)


class FormsTests(TestCase):
    def test_driver_creation_form(self) -> None:
        form_data = {
            "username": "mecho",
            "password1": "Secretpw_1",
            "password2": "Secretpw_1",
            "first_name": "Mister",
            "last_name": "Echo",
            "license_number": "HEL12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form(self) -> None:
        form = DriverSearchForm(
            data={"username": "mecho"}
        )
        self.assertTrue(form.is_valid())

    def test_car_search_form(self) -> None:
        form = CarSearchForm(
            data={"model": "Cybertruck"}
        )
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self) -> None:
        form = ManufacturerSearchForm(
            data={"name": "Tesla"}
        )
        self.assertTrue(form.is_valid())

    def test_invalid_license_number(self) -> None:
        form_data = {
            "license_number": "12345678",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
