from django.test import TestCase

from taxi.forms import DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "RDS87649"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

# class DriverLicenseUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Driver
#         fields = ["license_number"]
#
#     def clean_license_number(self):
#         return validate_license_number(self.cleaned_data["license_number"])
#
#
# def validate_license_number(
#     license_number,
# ):  # regex validation is also possible here
#     if len(license_number) != 8:
#         raise ValidationError("License number should consist of 8 characters")
#     elif not license_number[:3].isupper() or not license_number[:3].isalpha():
#         raise ValidationError("First 3 characters should be uppercase letters")
#     elif not license_number[3:].isdigit():
#         raise ValidationError("Last 5 characters should be digits")
#
#     return license_number