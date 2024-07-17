from django.test import TestCase
from unittest import mock
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarForm,
)
from taxi.models import Driver, Manufacturer
from taxi.templatetags.query_transform import query_transform


class DriverCreatingFormTest(TestCase):

    @staticmethod
    def get_form_data(**overrides):
        form_data = {
            "username": "new_user",
            "password1": "poiuytre123456",
            "password2": "poiuytre123456",
            "license_number": "TST23456",
            "first_name": "John",
            "last_name": "Doe",
        }
        form_data.update(overrides)
        return form_data

    def test_driver_creation_form_is_valid(self):
        form = DriverCreationForm(data=self.get_form_data())
        self.assertTrue(form.is_valid())

    def test_form_saves_new_driver_instance_successfully(self):
        form = DriverCreationForm(data=self.get_form_data())
        if form.is_valid():
            driver = form.save()
            self.assertIsInstance(driver, Driver)
            self.assertEqual(driver.username, form.cleaned_data["username"])

    def test_form_is_invalid_with_incorrect_license_number(self):
        form = DriverCreationForm(
            data=self.get_form_data(license_number="tys12")
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormTest(TestCase):
    def test_form_is_valid_with_all_required_fields_filled_correctly(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        driver1 = Driver.objects.create(
            username="driver1", password="password", license_number="RTY12345"
        )
        driver2 = Driver.objects.create(
            username="driver2", password="password", license_number="RTY12346"
        )
        form_data = {
            "model": "Test Model",
            "manufacturer": manufacturer.id,
            "drivers": [driver1.id, driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_with_missing_required_fields(self):
        form_data = {"model": "", "manufacturer": "", "drivers": []}
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_handles_empty_queryset_for_drivers(self):
        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        form_data = {
            "model": "Test Model",
            "manufacturer": manufacturer.id,
            "drivers": [],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())


class LicenseNumberUpgradeTest(TestCase):
    def test_valid_license_number_is_accepted(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_saves_with_valid_license_number(self):
        driver = Driver.objects.create(
            username="testuser",
            license_number="XYZ98765"
        )
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data, instance=driver)
        self.assertTrue(form.is_valid())
        updated_driver = form.save()
        self.assertEqual(updated_driver.license_number, "ABC12345")

    def test_license_number_invalid_raises_error(self):
        form_data = {"license_number": "ABC1234"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class SearchFormsTest(TestCase):
    def test_form_accepts_valid_username_input(self):
        form_data = {"username": "validuser"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "validuser")

    def test_form_handles_excessively_long_username_input(self):
        form_data = {"username": "a" * 256}
        form = DriverSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_handles_special_characters_in_username(self):
        form_data = {"username": "user!@#"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "user!@#")

    def test_placeholder_text_rendered_correctly(self):
        form = DriverSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )

    def test_form_field_not_required(self):
        form = DriverSearchForm()
        self.assertFalse(form.fields["username"].required)

    def test_form_handles_empty_input_gracefully(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_updates_query_parameters_with_new_values(self):
        request = mock.Mock()
        request.GET = {"param1": "value1", "param2": "value2"}
        result = query_transform(request, param1="new_value1", param3="value3")
        self.assertEqual(
            result,
            "param1=new_value1&param2=value2&param3=value3"
        )
