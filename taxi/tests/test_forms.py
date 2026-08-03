from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverUsernameSearchForm


class FormsTests(TestCase):
    def test_user_dont_created_with_wrong_license_number(self):
        form = DriverCreationForm(
            data={
                "username": "123",
                "password1": "123password__!",
                "password2": "123password__!",
                "first_name": "driver",
                "last_name": "name",
                "license_number": "123"
            }
        )

        self.assertFalse(form.is_valid())

    def test_user_created_with_correct_license_number(self):
        form = DriverCreationForm(
            data={
                "username": "123",
                "password1": "123password__!",
                "password2": "123password__!",
                "first_name": "driver",
                "last_name": "name",
                "license_number": "ABC12345"
            }
        )

        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(
            get_user_model()
            .objects
            .filter(license_number="ABC12345")
            .count(), 1
        )


class SearchFormTest(TestCase):
    def test_driver_form_is_valid(self):
        form = DriverUsernameSearchForm(
            data={"username": "john"}
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            "john"
        )
