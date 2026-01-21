from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_licence_first_last_name_is_valid(self) -> None:
        form_data = {
            "username": "usertest",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "LWE45642",
            "first_name": "Nametest",
            "last_name": "Lasttest",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid(), msg=form.errors)

        expected_fields = ["username", "first_name",
                           "last_name", "license_number"]
        for field in expected_fields:
            self.assertIn(field, form.cleaned_data)
            self.assertEqual(
                form.cleaned_data[field],
                form_data[field],
                msg=f"Field '{field}' doesn't match:"
                    f" {form.cleaned_data[field]} != {form_data[field]}"
            )
