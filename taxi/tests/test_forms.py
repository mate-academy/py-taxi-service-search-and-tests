from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverSearchForm


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "testpass1",
            "password2": "testpass1",
            "license_number": "ABC12345",
            "first_name": "Test first",
            "last_name": "Test last",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form_is_valid(self):
        form_data = {"username": "test_model"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue("username" in form.fields)
