from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django import forms

from taxi.models import Manufacturer
from taxi.forms import (
    CarCreateForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ListSearchForm
)


class TestCarCreateForm(TestCase):
    def test_from_and_widget(self):
        for i in range(3):
            get_user_model().objects.create_user(
                username=f"test_{i}",
                password="Password_1",
                license_number=f"ABC1234{i}"
            )
        manufacturer = Manufacturer.objects.create(name="some manufacturer")

        data = {
            "model": "fiesta",
            "manufacturer": manufacturer,
            "drivers": get_user_model().objects.all(),
        }
        form = CarCreateForm(data=data)
        self.assertTrue(form.is_valid())
        car = form.save()
        self.assertEqual(car.model, "fiesta")
        self.assertEqual(car.manufacturer, manufacturer)
        self.assertEqual(
            str(car.drivers.all()),
            str(get_user_model().objects.all())
        )
        self.assertIsInstance(
            form.fields["drivers"], forms.ModelMultipleChoiceField)
        self.assertIsInstance(
            form.fields["drivers"].widget, forms.CheckboxSelectMultiple)


class TestDriversForm(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "test_user",
            "password": "<PASSWORD>",
            "first_name": "Johnathan",
            "last_name": "Limited",
            "email": "jijo@gmail.com",
            "license_number": "ABC12345"
        }

    def test_form_with_valid_data(self):
        form = DriverCreationForm(self.user_data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(
            driver.license_number, self.user_data["license_number"]
        )
        self.assertNotIn("license_number", form.errors)
        self.assertEqual(
            form.cleaned_data["license_number"],
            self.user_data["license_number"]
        )
        self.assertEqual(form.fields["license_number"].max_length, 8)
        self.assertEqual(form.fields["license_number"].min_length, 8)

    def test_form_with_invalid_data(self):
        license_numbers = [
            "1ASD1234",
            "ADD4",
            "FFD123456",
            "FQDF3456",
            "azX12334"
        ]
        for license_number in license_numbers:

            self.user_data["license_number"] = license_number
            form = DriverCreationForm(self.user_data)
            self.assertFalse(form.is_valid())

    def test_short_username(self):
        self.user_data["username"] = "te"
        form = DriverCreationForm(self.user_data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "username",
            "Username is too short. Min. length is 3 symbols."
        )


class TestLicenseUpdateForm(TestCase):
    def setUp(self):
        user_data = {
            "username": "test_user",
            "password": "<PASSWORD>",
            "first_name": "Johnathan",
            "last_name": "Limited",
            "email": "jijo@gmail.com",
            "license_number": "ABC12345"
        }
        user = get_user_model().objects.create_user(**user_data)
        client = Client()
        client.force_login(user)

    def test_form_with_valid_data(self):
        new_license_number = {"license_number": "XYZ00123"}
        form = DriverLicenseUpdateForm(data=new_license_number)
        self.assertTrue(form.is_valid())
        self.assertNotIn("license_number", form.errors)
        self.assertEqual(
            form.cleaned_data["license_number"],
            new_license_number["license_number"]
        )
        self.assertEqual(form.fields["license_number"].max_length, 8)
        self.assertEqual(form.fields["license_number"].min_length, 8)

    def test_form_with_invalid_data(self):
        new_license_numbers = [
            {"license_number": ""},
            {"license_number": "ABC1"},
            {"license_number": "ABB123456"},
            {"license_number": "1BC12345"},
            {"license_number": "ABC1234a"},
            {"license_number": "AzC12343"}
        ]
        for license_number in new_license_numbers:
            form = DriverLicenseUpdateForm(data=license_number)
            self.assertFalse(form.is_valid())
            self.assertIn("license_number", form.errors)

    def test_form_errors_with_invalid_data(self):
        license_number_1 = {"license_number": "AzC12343"}
        error_message_1 = ("The first 3 characters of the license number "
                           "must be uppercase letters!")

        form = DriverLicenseUpdateForm(data=license_number_1)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertFormError(form, "license_number", error_message_1)

        license_number_2 = {"license_number": "AAC1234a"}
        error_message_2 = "Last 5 characters must be digits!"

        form = DriverLicenseUpdateForm(data=license_number_2)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertFormError(form, "license_number", error_message_2)


class TestSearchForm(TestCase):
    def test_with_valid_data(self):
        data = {"search_data": "test data"}

        form = ListSearchForm(placeholder="Test search", data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["search_data"],
            data["search_data"]
        )
        self.assertEqual(form.fields["search_data"].max_length, 100)
        self.assertEqual(form.fields["search_data"].label, "")
        self.assertIsInstance(
            form.fields["search_data"].widget,
            forms.TextInput
        )
        self.assertIsInstance(form.fields["search_data"], forms.CharField)
        self.assertEqual(
            form.fields["search_data"].widget.attrs["placeholder"],
            "Test search")

    def test_with_invalid_data(self):
        data = {"search_data": "test" * 30}
        data_length = len(data["search_data"])
        error_message = (f"Ensure this value has at most 100 characters "
                         f"(it has {data_length}).")
        form = ListSearchForm(placeholder="Test search", data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, "search_data", error_message)
