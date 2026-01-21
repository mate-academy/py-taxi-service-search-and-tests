from django.urls import reverse
from django.test import TestCase, SimpleTestCase
from django.core.exceptions import ValidationError
from taxi.forms import (CarForm, DriverCreationForm,
                        DriverLicenseUpdateForm, validate_license_number)
from taxi.models import Driver, Car, Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer")
        self.driver1 = Driver.objects.create_user(
            username="driver1", password="testpass", license_number="ABC12345")
        self.driver2 = Driver.objects.create_user(
            username="driver2", password="testpass", license_number="DEF67890")

    def test_car_form_valid_data(self):
        form = CarForm(data={
            "model": "Test Model",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk]
        })
        self.assertTrue(form.is_valid())

    def test_car_form_no_data(self):
        form = CarForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid_data(self):
        form = DriverCreationForm(data={
            "username": "testuser",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe"
        })
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license_number(self):
        form = DriverCreationForm(data={
            "username": "testuser",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "license_number": "ABC1234",
            "first_name": "John",
            "last_name": "Doe"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid_data(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid_data(self):
        form = DriverLicenseUpdateForm(data={"license_number": "invalid"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class ValidateLicenseNumberTest(SimpleTestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_invalid_length_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AB12345")

    def test_invalid_format_license_number(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABc12345")


class DriverListViewTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create_user(
            username="driver1", password="testpass", license_number="ABC12345")
        self.driver2 = Driver.objects.create_user(
            username="driver2", password="testpass", license_number="DEF67890")
        self.client.login(username="driver1", password="testpass")

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)

    def test_driver_list_view_with_search(self):
        response = self.client.get(reverse(
            "taxi:driver-list") + "?username=driver1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)
