from django.test import TestCase

from taxi.forms import (
    CarForm, DriverCreationForm, DriverLicenseUpdateForm,
    SearchListForm
)
from taxi.models import Driver, Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(
            first_name="btest_name",
            last_name="btest_last_name",
            username="busername",
            email="btest@gmail.com",
            license_number="FHG17564"
        )
        self.driver2 = Driver.objects.create(
            first_name="atest_name",
            last_name="atest_last_name",
            username="ausername",
            email="atest@gmail.com",
            license_number="FHG12939"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="btest",
            country="btest country"
        )

    def test_renew_form_date_field_label(self):
        form = CarForm()
        self.assertTrue(
            form.fields['drivers'].label is None or form.fields[
                'drivers'].label == 'drivers'
        )

    def test_valid_form(self):
        data = {
            "model": "model_test",
            "manufacturer": self.manufacturer,
            "drivers": [self.driver1.pk, self.driver2.pk],
        }
        form = CarForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_model(self):
        data = {
            "manufacturer": self.manufacturer,
            "drivers": [self.driver1.pk, self.driver2.pk],
        }
        form = CarForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)

    def test_invalid_form_missing_manufacturer(self):
        data = {
            "model": "model_test",
            "drivers": [self.driver1.pk, self.driver2.pk],
        }
        form = CarForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("manufacturer", form.errors)

    def test_invalid_form_invalid_tags(self):
        data = {
            "model": "Model",
            "manufacturer": self.manufacturer,
            "drivers": [999],  # Invalid tag ID
        }
        form = CarForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('drivers', form.errors)


class DriverCreationFormTest(TestCase):
    def test_form_is_valid(self):
        data = {
            "first_name": "User",
            "last_name": "Last user",
            "license_number": "THF12645",
            "username": "username124",
            "email": "user@gmail.com",
            "password1": "testpassword",
            "password2": "testpassword"
        }
        form = DriverCreationForm(data)
        self.assertTrue(form.is_valid())

    def test_form_is_valid_missing_not_required_fields(self):
        data = {
            "license_number": "THF12645",
            "username": "username124",
            "password1": "testpassword",
            "password2": "testpassword"
        }
        form = DriverCreationForm(data)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_missing_license_number(self):
        data = {
            "username": "username124",
            "password1": "testpassword",
            "password2": "testpassword"
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_form_is_not_valid_missing_username(self):
        data = {
            "license_number": "THF12645",
            "password1": "testpassword",
            "password2": "testpassword"
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_is_not_valid_missing_password1(self):
        data = {
            "license_number": "THF12645",
            "username": "username124",
            "password2": "testpassword"
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_form_is_not_valid_password2_now_equal_password1(self):
        data = {
            "license_number": "THF12645",
            "username": "username124",
            "password1": "testpassword",
            "password2": "lkfjdas"
        }
        form = DriverCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_validation_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("TES12345").is_valid())

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertFalse(self.create_form("TES123456").is_valid())

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertFalse(self.create_form("TES1234").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("TE123456").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("TEST2345").is_valid())


class SearchListFormTest(TestCase):
    @staticmethod
    def create_form(search):
        return SearchListForm(
            data={"search": search}
        )

    def test_form_is_valid(self):
        self.assertTrue(self.create_form("lkfjdlkasjl").is_valid())

    def test_form_is_not_valid_length(self):
        form = self.create_form(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed "
            "do eiusmod tempor incididunt ut labore et dolore magna "
            "aliqua.Ut enim ad minim veniam, quis nostrud exercitation "
            "ullamco laboris nisi ut aliquip ex ea commodo consequat."
            " Duis aute irure dolor in reprehenderit in voluptate velit "
            "esse cillum dolore eu fugiat nulla pariatur. Excepteur sint "
            "occaecat cupidatat non proident, sunt in culpa qui officia "
            "deserunt mollit ani"
        )
        self.assertFalse(form.is_valid())

    def test_form_is_valid_with_empty_search(self):
        form = self.create_form("")
        form.is_valid()
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_search_lable(self):
        form = self.create_form("")
        self.assertTrue(
            form.fields['search'].label is None
            or form.fields['search'].label == ""
        )

    def test_search_widget_placeholder(self):
        form = self.create_form("")
        self.assertEqual(
            form.fields['search'].widget.attrs["placeholder"],
            "Search..."
        )
