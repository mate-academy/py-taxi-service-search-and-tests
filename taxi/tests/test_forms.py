from django.test import TestCase

from taxi.forms import (
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    DriverCreationForm
)


class CarSearchFormsTest(TestCase):
    def test_car_search_form_empty(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_car_search_form_with_model_name(self):
        form = CarSearchForm(
            data={"model": "Edge"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Edge")


class DriverSearchFormsTest(TestCase):
    def test_driver_search_form_empty(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_driver_search_form_with_username(self):
        form = DriverSearchForm(
            data={"username": "John"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "John")


class DriverCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {
            "username": "JohnD",
            "license_number": "FAR12765",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "test_password",
            "password2": "test_password",
        }

    def test_driver_creation_form_with_valid_data(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_create_driver(self):
        form = DriverCreationForm(data=self.form_data)
        driver = form.save()
        self.assertEqual(driver.username, "JohnD")
        self.assertEqual(driver.license_number, "FAR12765")
        self.assertEqual(driver.first_name, "John")
        self.assertEqual(driver.last_name, "Doe")
        self.assertTrue(driver.check_password("test_password"))


class ManufacturerSearchFormsTest(TestCase):
    def test_manufacturer_search_form_empty(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_manufacturer_search_form_with_model_name(self):
        form = ManufacturerSearchForm(
            data={
                "name": "Ford",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Ford")
