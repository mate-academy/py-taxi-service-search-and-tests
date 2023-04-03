from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarModelSearchForm
)


class DriverTest(TestCase):

    def test_driver_creation_with_license_first_last(self):
        form_data = {
            "username": "test_user",
            "password1": "test12345",
            "password2": "test12345",
            "license_number": "TES12345",
            "first_name": "Test",
            "last_name": "Case",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseTest(TestCase):

    def test_driver_license_update(self):
        form = DriverLicenseUpdateForm()
        expected_fields = ["license_number"]
        self.assertSequenceEqual(list(form.fields), expected_fields)

    def test_wrong_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TEST1234"})
        self.assertFalse(form.is_valid())

    def test_right_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TES12345"})
        self.assertTrue(form.is_valid())

    def test_all_wrong_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TEsq12342Fsa4"})
        self.assertFalse(form.is_valid())


class DriverSearchFormTest(TestCase):
    def setUp(self):
        self.form_data = {"username": "john.wik"}

    def test_valid_search(self):
        form = DriverSearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_empty_search(self):
        form = DriverSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_case_insensitive_search(self):
        form = DriverSearchForm(data={"username": "JoHN.wik"})
        self.assertTrue(form.is_valid())


class CarModelSearchFormTest(TestCase):
    def setUp(self):
        self.form_data = {"model": "fusion"}

    def test_valid_search(self):
        form = CarModelSearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_empty_search(self):
        form = CarModelSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_case_insensitive_search(self):
        form = CarModelSearchForm(data={"model": "fuSiOn"})
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def setUp(self):
        self.form_data = {"name": "Audi"}

    def test_valid_search(self):
        form = CarModelSearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_empty_search(self):
        form = CarModelSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_case_insensitive_search(self):
        form = CarModelSearchForm(data={"name": "AuDI"})
        self.assertTrue(form.is_valid())
