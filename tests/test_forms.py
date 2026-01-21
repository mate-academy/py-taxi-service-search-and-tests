from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm,
                        DriverSearchForm)
from taxi.models import Driver


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "ABC12345",
            "first_name": "Test first",
            "last_name": "Test last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="12345",
            license_number="ABC12345"
        )

    def test_form_driver_update_is_valid(self):
        form = DriverLicenseUpdateForm(
            instance=self.driver,
            data={"license_number": "DEF67890"})
        self.assertTrue(form.is_valid())


class DriverSearchFormTest(TestCase):
    def test_model_field_present(self):
        field = "username"
        form_data = {field: "test_model"}
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(field in form.fields)
