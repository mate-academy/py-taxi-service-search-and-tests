from django.test import TestCase


from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class DriverFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "john",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "AAA11111",
        }

    def test_driver_creation_form(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_invalid_license_number(self):
        self.form_data["license_number"] = "12345"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTests(TestCase):
    @staticmethod
    def create_form(license_number: str):
        return DriverCreationForm(
            data={
                "license_number": license_number,
                "first_name": "John",
                "last_name": "Doe",
                "username": "john",
                "password1": "user12test",
                "password2": "user12test",
            }
        )

    def test_is_valid_license_number(self):
        form = self.create_form("AAA12345")
        self.assertTrue(form.is_valid())

    def test_first_3_upper_letter_case(self):
        form = self.create_form("11111")
        self.assertFalse(form.is_valid())

    def test_5_last_digits(self):
        form = self.create_form("AAA1111q")
        self.assertFalse(form.is_valid())

    def test_min_length_license_number(self):
        form = self.create_form("AAA111")
        self.assertFalse(form.is_valid())

    def test_max_length_license_number(self):
        form = self.create_form("AAA11111111")
        self.assertFalse(form.is_valid())
