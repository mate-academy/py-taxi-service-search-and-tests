from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverSearchForm


class FormsTests(TestCase):
    def test_driver_creation_form_license_first_last_name_is_valid(self):
        form_data = {
            "username": "new_test_username",
            "password1": "user13test",
            "password2": "user13test",
            "license_number": "ADT12345",
            "first_name": "first_name",
            "last_name": "last_name",
        }
        form = DriverCreationForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )


class DriverSearchFormTests(TestCase):
    def test_form_is_valid_username(self):
        form_data = {"username": "new_test_username"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "new_test_username")

    def test_form_is_valid_without_username(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_placeholder_in_widget(self):
        form = DriverSearchForm()
        placeholder = form.fields["username"].widget.attrs["placeholder"]
        self.assertEqual(placeholder, "Search by username")
