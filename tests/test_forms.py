from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        DriverSearchForm)


class FormsTest(TestCase):
    def test_driver_creation_form(self) -> None:
        form_data = {
            "username": "user",
            "password1": "test_1234",
            "password2": "test_1234",
            "first_name": "Firstname",
            "last_name": "LastName",
            "license_number": "QWE12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_invalid_license_number(self) -> None:
        form_data = {
            "license_number": "12345678",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_search_form(self) -> None:
        form = DriverSearchForm(
            data={"username": "user"}
        )
        self.assertTrue(form.is_valid())

    def test_car_search_form(self) -> None:
        form = CarSearchForm(
            data={"model": "ford"}
        )
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self) -> None:
        form = ManufacturerSearchForm(
            data={"name": "GM"}
        )
        self.assertTrue(form.is_valid())
