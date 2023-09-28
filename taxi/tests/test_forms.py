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
