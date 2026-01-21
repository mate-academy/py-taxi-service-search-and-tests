from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    fixtures = ["taxi/fixtures/taxi_service_db_data.json", ]

    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.get(id=1)
        self.driver_1 = get_user_model().objects.get(id=1)
        self.driver_2 = get_user_model().objects.get(id=2)

    def test_car_form_valid(self) -> None:
        form_data = {
            "model": "Model_name",
            "manufacturer": self.manufacturer,
            "drivers": [self.driver_1, self.driver_2]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["model"],
            form_data["model"]
        )
        self.assertEqual(
            form.cleaned_data["manufacturer"],
            form_data["manufacturer"]
        )
        self.assertEqual(
            list(form.cleaned_data["drivers"]),
            list(form_data["drivers"])
        )

    def test_car_form_invalid_no_drivers(self) -> None:
        form_data = {
            "model": "Model_name",
            "manufacturer": self.manufacturer,
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_form_invalid_no_model(self) -> None:
        form_data = {
            "manufacturer": self.manufacturer,
            "drivers": [self.driver_1, self.driver_2]
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_form_invalid_no_manufacturer(self) -> None:
        form_data = {
            "model": "Model_name",
            "drivers": [self.driver_1, self.driver_2]
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverCreationFormTest(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "Testuser",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
            "password1": "test123test",
            "password2": "test123test"
        }

    def test_driver_form_valid_with_first_and_last_names(self) -> None:
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_form_valid(self) -> None:
        del self.form_data["first_name"], self.form_data["last_name"]
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_no_license_number(self) -> None:
        del self.form_data["license_number"]
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_car_form_invalid_license_number(self) -> None:
        self.form_data["license_number"] = "ABC1234"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create(
            username="Test",
            license_number="ABC12345"
        )

    def test_driver_license_update_valid(self) -> None:
        form_data = {"license_number": "DEF67890"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_invalid_less_than_8_chars(self) -> None:
        form_data = {"license_number": "DEF678"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_invalid_more_than_8_chars(self) -> None:
        form_data = {"license_number": "DEF678901"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_invalid_first_3_not_uppercase(self) -> None:
        form_data = {"license_number": "def67890"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_invalid_last_five_not_digits(self) -> None:
        form_data = {"license_number": "ABC12av2"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertFalse(form.is_valid())


class SearchFormsTest(TestCase):
    def test_driver_search_form(self) -> None:
        form_data = {"username": "test_user"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form(self) -> None:
        form_data = {"model": "test_model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form(self) -> None:
        form_data = {"name": "test_name"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
