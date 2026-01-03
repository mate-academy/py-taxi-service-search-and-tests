from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
)


class FormsTests(TestCase):
    def test_driver_create_driver_form_with_license_number_is_valid(self):
        self.driver_data = {
            "username": "new_driver",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "QWE12345",
            "first_name": "test_first",
            "last_name": "test_last",
        }
        form = DriverCreationForm(data=self.driver_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.driver_data)


class SearchFormsTests(TestCase):
    def test_manufacturer_search_form_with_name(self):
        form = ManufacturerSearchForm(
            data={"name": "mazda"}
        )

        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_without_name(self):
        form = ManufacturerSearchForm(
            data={"name": ""}
        )

        self.assertTrue(form.is_valid())

    def test_car_search_form_with_model(self):
        form = CarSearchForm(
            data={"model": "mx-30"}
        )

        self.assertTrue(form.is_valid())

    def test_car_search_form_without_model(self):
        form = CarSearchForm(
            data={"model": ""}
        )

        self.assertTrue(form.is_valid())

    def test_driver_search_form_with_username(self):
        form = DriverSearchForm(
            data={"username": "test_user"}
        )

        self.assertTrue(form.is_valid())

    def test_driver_search_form_without_username(self):
        form = DriverSearchForm(
            data={"username": ""}
        )

        self.assertTrue(form.is_valid())
