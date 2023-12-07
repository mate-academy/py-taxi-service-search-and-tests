from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Driver

car_url = reverse("taxi:car-list")
driver_url = reverse("taxi:driver-list")
manufacturer_url = reverse("taxi:manufacturer-list")


class FormTests(TestCase):
    def test_driver_creation_form_with_license(self):
        form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "first_name": "firsttest",
            "last_name": "lasttest",
            "license_number": "TTT12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_valid(self):
        user = get_user_model().objects.create(username="test_user")
        form_data = {
            "license_number": "LIO12345",
        }
        form = DriverLicenseUpdateForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid())


class FormSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_search_driver_by_username(self):
        Driver.objects.create(
            username="testuser", password="testpass", license_number="LIO1234"
        )

        searched_name = "test_user"
        response = self.client.get(driver_url, {"username": searched_name})
        self.assertEqual(response.status_code, 200)
        context = Driver.objects.filter(
            username__icontains=searched_name
        )
        self.assertEqual(
            list(response.context["driver_list"]), list(context)
        )

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="test"
        )
        searched_name = "test"
        response = self.client.get(manufacturer_url, name=searched_name)
        self.assertEqual(response.status_code, 200)
        context = Manufacturer.objects.filter(
            name__icontains=searched_name
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]), list(context)
        )


class DriverLicenseValidationTests(TestCase):
    def test_license_number_should_consist_8_characters(self):
        form_data = {
            "license_number": "LIO1234",
        }
        DriverLicenseUpdateForm(data=form_data)
        self.assertRaisesMessage(
            ValidationError,
            "License number should consist of 8 characters"
        )

    def test_license_number_first_3_character_should_be_uppercase_letter(self):
        form_data_base = {
            "license_number1": "lio12345",
            "license_number2": "Lio12345",
            "license_number3": "LIo12345",
        }
        for form_data in form_data_base:
            DriverLicenseUpdateForm(data=form_data)
            self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
            )

    def test_license_number_last_5_characters_should_be_digits(self):
        form_data_base = {
            "license_number1": "LIO_2345",
            "license_number2": "LIO1_345",
            "license_number3": "LIO12_45",
            "license_number4": "LIO123_5",
            "license_number5": "LIO1234_",
        }
        for form_data in form_data_base:
            DriverLicenseUpdateForm(data=form_data)
            self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits"
            )
