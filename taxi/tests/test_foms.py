from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Car, Driver, Manufacturer
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    SearchForm
)


class CarFormTests(TestCase):

    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.user1 = get_user_model().objects.create_user(
            username="user1",
            password="password1",
            license_number="tes12345"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2",
            password="password2",
            license_number="tes22345"
        )

    def test_valid_car_form(self) -> None:
        form_data = {
            "model": "Test Car",
            "manufacturer": self.manufacturer,
            "drivers": [self.user1, self.user2],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_fields(self) -> None:
        form = CarForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_invalid_drivers(self) -> None:
        form_data = {
            "model": "Test Car",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user1, 9999],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)

    def test_display_of_form(self) -> None:
        form = CarForm()
        self.assertIn('name="model"', form.as_p())
        self.assertIn('name="manufacturer"', form.as_p())
        self.assertIn('name="drivers"', form.as_p())


class DriverCreationFormTests(TestCase):

    def test_valid_driver_creation_form(self) -> None:
        form_data = {
            "username": "new_user",
            "license_number": "TES12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "password1": "user12test",
            "password2": "user12test",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_fields(self) -> None:
        form = DriverCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_invalid_license_number(self) -> None:
        form_data = {
            "username": "new_user",
            "license_number": "INVALID",
            "first_name": "Test first",
            "last_name": "Test last",
            "password1": "user12test",
            "password2": "user12test",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):

    def test_valid_license_update_form(self) -> None:
        form_data = {
            "license_number": "TES12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_field(self) -> None:
        form = DriverLicenseUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_invalid_license_number(self) -> None:
        form_data = {
            "license_number": "WRONG_NUMBER",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class SearchFormTests(TestCase):

    def test_valid_search_form(self) -> None:
        form_data = {
            "search": "Test Query",
        }
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_search_field(self) -> None:
        form = SearchForm(data={})
        self.assertTrue(form.is_valid())
