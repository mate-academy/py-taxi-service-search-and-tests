from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverSearchForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_additional_fields(self):
        """
        Test driver creation form with license_number, first_name and last_name
        """
        form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "ABC54321",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_validate_license_number(self):
        form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "license_number": "ABC54321",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data["license_number"] = "ABC5432"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "AB354321"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data["license_number"] = "ABCD4321"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_search_form(self):
        get_user_model().objects.create_user(
            username="Test1",
            password="test_driver",
            license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="Test2",
            password="test_driver",
            license_number="ABC12346"
        )
        form_data = {"username": "test2"}

        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
