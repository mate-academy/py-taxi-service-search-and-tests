from django.contrib.auth import get_user_model, forms
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    DriverLicenseUpdateForm, CarForm
)
from taxi.models import Manufacturer


class CarFormsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.driver1 = get_user_model().objects.create_user(
            username="new_driver1",
            password="new_password!",
            license_number="ABC12345",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="new_driver2",
            password="new_password!",
            license_number="DEF67890",
        )

    def test_form_saves_car_with_selected_drivers(self):
        form = CarForm(data={
            "model": "Toyota Camry",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk],
        })

        self.assertTrue(form.is_valid(), form.errors)

        car = form.save()

        self.assertEqual(car.model, "Toyota Camry")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertCountEqual(
            car.drivers.all(),
            [self.driver1, self.driver2],
        )

    def test_missing_required_fields(self):
        form = CarForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)
        self.assertIn("manufacturer", form.errors)
        self.assertIn("drivers", form.errors)

    def test_invalid_driver_id(self):
        form = CarForm(data={
            "model": "Toyota Camry",
            "manufacturer": self.manufacturer.pk,
            "drivers": [999999],
        })

        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)


class DriverFormsTests(TestCase):
    def test_form_creates_driver(self):
        form_data = {
            "username": "new_driver",
            "first_name": "new_first",
            "last_name": "new_last",
            "password1": "new_password",
            "password2": "new_password",
            "license_number": "ABC12345",
        }

        form = DriverCreationForm(data=form_data)
        driver = form.save()

        self.assertEqual(driver.username, "new_driver")
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertEqual(driver.first_name, "new_first")
        self.assertEqual(driver.last_name, "new_last")
        self.assertTrue(driver.check_password("new_password"))

    def test_form_is_valid(self):
        form_data = {
            "username": "new_driver",
            "first_name": "new_first",
            "last_name": "new_last",
            "password1": "new_password",
            "password2": "new_password",
            "license_number": "ABC12345",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_with_invalid_length(self):
        form_data = {
            "username": "new_driver",
            "first_name": "new_first",
            "last_name": "new_last",
            "password1": "new_password",
            "password2": "new_password",
            "license_number": "ABC1234",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_with_lowercase_prefix(self):
        form_data = {
            "username": "new_driver",
            "first_name": "new_first",
            "last_name": "new_last",
            "password1": "new_password",
            "password2": "new_password",
            "license_number": "abc12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_with_digits_in_prefix(self):
        form_data = {
            "username": "new_driver",
            "first_name": "new_first",
            "last_name": "new_last",
            "password1": "new_password",
            "password2": "new_password",
            "license_number": "A2C12345",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_with_letters_in_suffix(self):
        form_data = {
            "username": "new_driver",
            "first_name": "new_first",
            "last_name": "new_last",
            "password1": "new_password",
            "password2": "new_password",
            "license_number": "ABC1234f",
        }

        form = DriverCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="new_driver",
            first_name="new_first",
            last_name="new_last",
            password="new_password",
            license_number="ABC12345",
        )

    def test_form_updates_license_number(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "DEF67890"},
            instance=self.driver,
        )

        self.assertTrue(form.is_valid(), form.errors)

        driver = form.save()

        self.assertEqual(driver.license_number, "DEF67890")

    def test_license_number_with_invalid_length(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "DEF6789"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_with_lowercase_prefix(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "def67890"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_with_invalid_suffix(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "DEF67G90"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarSearchFormTests(TestCase):
    def test_empty_model_is_valid(self):
        form = CarSearchForm(data={"model": ""})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_valid_model_search(self):
        form = CarSearchForm(data={"model": "Toyota Camry"})

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["model"],
            "Toyota Camry",
        )

    def test_model_exceeding_max_length_is_invalid(self):
        form = CarSearchForm(data={"model": "A" * 256})

        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)

    def test_model_widget_placeholder(self):
        form = CarSearchForm()

        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model",
        )


class DriverSearchFormTests(TestCase):
    def test_empty_username_is_valid(self):
        form = DriverSearchForm(data={"username": ""})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_valid_username_search(self):
        form = DriverSearchForm(data={"username": "new_driver"})

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            "new_driver",
        )

    def test_username_exceeding_max_length_is_invalid(self):
        form = DriverSearchForm(data={"username": "A" * 256})

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_username_widget_placeholder(self):
        form = DriverSearchForm()

        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username",
        )


class ManufacturerSearchFormTests(TestCase):
    def test_empty_name_is_valid(self):
        form = ManufacturerSearchForm(data={"name": ""})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_valid_name_search(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["name"],
            "Toyota",
        )

    def test_name_exceeding_max_length_is_invalid(self):
        form = ManufacturerSearchForm(data={"name": "A" * 256})

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_name_widget_placeholder(self):
        form = ManufacturerSearchForm()

        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name",
        )
