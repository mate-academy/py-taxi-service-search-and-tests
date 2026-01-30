from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from taxi.models import Manufacturer
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    validate_license_number,
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm,
)


class BaseObjectsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="driver1", password="pass123", license_number="AXG65432"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2", password="pass123", license_number="ADH098765"
        )


class CarFormTest(BaseObjectsTest):
    def test_form_has_drivers_field(self):
        form = CarForm()
        self.assertIn("drivers", form.fields)
        self.assertEqual(
            type(form.fields["drivers"].widget).__name__,
            "CheckboxSelectMultiple"
        )

    def test_form_saves_with_selected_drivers(self):
        form_data = {
            "model": "X7",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        car = form.save()
        self.assertIn(self.driver1, car.drivers.all())
        self.assertIn(self.driver2, car.drivers.all())


class DriverCreationFormTest(BaseObjectsTest):
    def test_form_has_additional_fields(self):
        form = DriverCreationForm()
        self.assertIn("license_number", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)

    def test_form_creates_driver_successfully(self):
        form_data = {
            "username": "new_driver",
            "password1": "strongpass321",
            "password2": "strongpass321",
            "first_name": "James",
            "last_name": "Bond",
            "license_number": "AXE98765",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.username, "new_driver")
        self.assertEqual(driver.first_name, "James")
        self.assertEqual(driver.last_name, "Bond")
        self.assertEqual(driver.license_number, "AXE98765")

    def test_form_invalid_license_number(self):
        form_data = {
            "username": "new_driver",
            "password1": "strongpass321",
            "password2": "strongpass321",
            "first_name": "James",
            "last_name": "Bond",
            "license_number": "INVALID",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(BaseObjectsTest):
    def test_form_has_license_number_field(self):
        form = DriverLicenseUpdateForm(instance=self.driver1)
        self.assertIn("license_number", form.fields)

    def test_form_valid_with_correct_license_number(self):
        form = DriverLicenseUpdateForm(
            instance=self.driver1,
            data={"license_number": "AQF76543"}
        )
        self.assertTrue(form.is_valid())
        updated_driver = form.save()
        self.assertEqual(updated_driver.license_number, "AQF76543")

    def test_form_invalid_with_wrong_license_number(self):
        form = DriverLicenseUpdateForm(
            instance=self.driver1,
            data={"license_number": "INVALID"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class ValidateLicenseNumberTest(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("AXE12345"), "AXE12345")

    def test_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AXE1234")

    def test_invalid_prefix_not_uppercase(self):
        with self.assertRaises(ValidationError):
            validate_license_number("axe12345")

    def test_invalid_prefix_not_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("A1E12345")

    def test_invalid_sufix_not_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AXE12AB5")


class DriverUsernameSearchFormTest(TestCase):
    def test_form_has_username_field(self):
        form = DriverUsernameSearchForm()
        self.assertIn("username", form.fields)
        self.assertFalse(form.fields["username"].required)
        self.assertEqual(form.fields["username"].max_length, 255)

    def test_form_valid_with_username(self):
        form = DriverUsernameSearchForm(data={"username": "testuser"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_form_valid_without_username(self):
        form = DriverUsernameSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_form_invalid_with_long_username(self):
        long_username = "a" * 256
        form = DriverUsernameSearchForm(data={"username": long_username})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_widget_placeholder(self):
        form = DriverUsernameSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs.get("placeholder"),
            "Search by username"
        )


class CarModelSearchFormTest(TestCase):
    def test_form_has_model_field(self):
        form = CarModelSearchForm()
        self.assertIn("model", form.fields)
        self.assertFalse(form.fields["model"].required)
        self.assertEqual(form.fields["model"].max_length, 255)

    def test_form_valid_with_model(self):
        form = CarModelSearchForm(data={"model": "X7"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "X7")

    def test_form_valid_without_model(self):
        form = CarModelSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_form_invalid_with_long_model(self):
        long_model = "a" * 256
        form = CarModelSearchForm(data={"model": long_model})
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)

    def test_form_widget_placeholder(self):
        form = CarModelSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs.get("placeholder"),
            "Search by model"
        )


class ManufacturerNameSearchFormTest(TestCase):
    def test_form_has_name_field(self):
        form = ManufacturerNameSearchForm()
        self.assertIn("name", form.fields)
        self.assertFalse(form.fields["name"].required)
        self.assertEqual(form.fields["name"].max_length, 255)

    def test_form_valid_with_name(self):
        form = ManufacturerNameSearchForm(data={"name": "BMW"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "BMW")

    def test_form_valid_without_name(self):
        form = ManufacturerNameSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_form_invalid_with_long_name(self):
        long_name = "a" * 256
        form = ManufacturerNameSearchForm(data={"name": long_name})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_form_widget_placeholder(self):
        form = ManufacturerNameSearchForm()
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Search by name"
        )
