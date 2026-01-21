from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm
from taxi.models import Driver

DRIVERS_LIST_URL = reverse("taxi:driver-list")


class CreateDriverFormTests(TestCase):
    def test_driver_creation_form_with_first_last_name_license_is_valid(self):
        form_data = {
            "username": "test_driver",
            "password1": "qwerty123test",
            "password2": "qwerty123test",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "AAA12345"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverUpdateLicenseNumberFormTests(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_validation_license_number_with_valid_data(self):
        self.assertTrue(self.create_form("AAA12345").is_valid())

    def test_length_of_license_number_should_be_not_more_than_8(self):
        self.assertFalse(self.create_form("AAA123456").is_valid())

    def test_length_of_license_number_should_be_not_less_than_8(self):
        self.assertFalse(self.create_form("AAA1234").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("AA123456").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("AAAA2345").is_valid())


class SearchDriverFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")

        self.driver1 = Driver.objects.create(
            username="driver_one",
            license_number="AAA12345"
        )
        self.driver2 = Driver.objects.create(
            username="driver_two",
            license_number="AAB12345"
        )
        self.driver3 = Driver.objects.create(
            username="another_driver",
            license_number="ABB12345"
        )

    def test_search_no_query(self):
        response = self.client.get(DRIVERS_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver_one")
        self.assertContains(response, "driver_two")
        self.assertContains(response, "another_driver")

    def test_search_with_query(self):
        response = self.client.get(DRIVERS_LIST_URL, {"username": "one"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver_one")

    def test_search_with_exact_match_query(self):
        response = self.client.get(DRIVERS_LIST_URL,
                                   {"username": "another_driver"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "another_driver")
        self.assertNotContains(response, "driver_one")
        self.assertNotContains(response, "driver_two")

    def test_search_with_no_results(self):
        response = self.client.get(DRIVERS_LIST_URL,
                                   {"username": "nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "driver_one")
        self.assertNotContains(response, "driver_two")
        self.assertNotContains(response, "another_driver")
