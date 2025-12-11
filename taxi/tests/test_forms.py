from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Driver


class FormTests(TestCase):
    def test_driver_creation_form_with_parameters(self):
        form_data = {
            "username": "user1",
            "password1": "<Password123>",
            "password2": "<Password123>",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="John_Doe",
            password="test1234",
            license_number="XYZ12345",
            first_name="John",
            last_name="Doe"
        )

    def test_update_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"},
                                       instance=self.driver)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.license_number, "ABC12345")

    def test_update_short_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc1234"},
                                       instance=self.driver)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_first_digits_not_letters_and_not_capitalized(self):
        form = DriverLicenseUpdateForm(data={"license_number": "a2C12345"},
                                       instance=self.driver)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_last_five_digits_not_a_numbers(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC123fg"},
                                       instance=self.driver)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverCreationLicenseNumberFormTest(TestCase):
    def setUp(self):
        self.data = {
            "username": "new_driver",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "first_name": "Alice",
            "last_name": "Smith"
        }

    def test_create_valid_license_number(self):
        data = {**self.data, "license_number": "ABC12345"}
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.license_number, "ABC12345")

    def test_create_short_license_number(self):
        data = {**self.data, "license_number": "ABC12"}
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_first_digits_not_letters_and_not_capitalized(self):
        data = {**self.data, "license_number": "a2C12345"}
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_last_five_digits_not_a_numbers(self):
        data = {**self.data, "license_number": "ABC123fg"}
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
