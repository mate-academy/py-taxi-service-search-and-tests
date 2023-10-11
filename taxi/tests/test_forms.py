from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm
from taxi.models import Manufacturer


class TestFormsValidation(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test name", country="test country"
        )
        self.driver = get_user_model().objects.create_user(
            username="test user",
            first_name="test first_name",
            last_name="test last_name",
            password="testuser",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def tearDown(self) -> None:
        self.driver.license_number = "ABC12345"

    def test_form_update_license_is_valid(self) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12346"})
        self.assertTrue(form.is_valid())

    def test_form_update_license_is_invalid_when_length_more_than_9(
        self,
    ) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "ABC123467"})
        self.assertFalse(form.is_valid())

    def test_form_update_license_is_invalid_when_length_lower_than_8(
        self,
    ) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "ABC1234"})
        self.assertFalse(form.is_valid())

    def test_form_update_license_is_invalid_when_first_3_are_not_letters(
        self,
    ) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "12312346"})
        self.assertFalse(form.is_valid())

    def test_form_update_license_is_invalid_when_first_3_are_lowercase_letters(
        self,
    ) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "abc12346"})
        self.assertFalse(form.is_valid())

    def test_form_update_license_is_invalid_when_last_5_are_not_numbers(
        self,
    ) -> None:
        form = DriverLicenseUpdateForm(data={"license_number": "ABCABCDE"})
        self.assertFalse(form.is_valid())

    def test_form_car_is_valid(self):
        form_data = {
            "model": "test model",
            "manufacturer": self.manufacturer,
            "drivers": [self.driver],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_driver_creation_is_valid(self):
        form_data = {
            "username": "usertesting",
            "password1": "1qacxz8sesad",
            "password2": "1qacxz8sesad",
            "license_number": "ABC12346",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
