from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer


class DataFormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name(self):
        form_data = {
            "username": "test_username",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "LLL98764",
            "first_name": "test_first_name",
            "last_name": "test_last_name"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

        invalid_form_data1 = form_data.copy()
        invalid_form_data1["license_number"] = "AA965432"
        form = DriverCreationForm(data=invalid_form_data1)
        self.assertFalse(form.is_valid())

        invalid_form_data2 = form_data.copy()
        invalid_form_data2["license_number"] = "AAAA6543"
        form = DriverCreationForm(data=invalid_form_data2)
        self.assertFalse(form.is_valid())

        invalid_form_data3 = form_data.copy()
        invalid_form_data3["license_number"] = "AAAA96543"
        form = DriverCreationForm(data=invalid_form_data3)
        self.assertFalse(form.is_valid())

    def test_valid_license_number(self):
        form_data = {
            "license_number": "LLL98765"
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_license_number(), "LLL98765")

    def test_invalid_license_number(self):
        form_data = {
            "license_number": "LA55367"
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class SearchFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_driver_search(self):
        get_user_model().objects.create(
            username="test_username1",
            password="test_password1",
            license_number="AAA84930"
        )
        get_user_model().objects.create(
            username="test_username2",
            password="test_password2",
            license_number="AAA93876"
        )

        search_request = "test_username1"
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": search_request}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_username1")

        search_request = "not_exist_username"
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": search_request}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "")

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name1",
            country="test_country1"
        )
        Car.objects.create(model="test_model_1", manufacturer=manufacturer)
        Car.objects.create(model="test_model_2", manufacturer=manufacturer)

        search_request = "test_model_1"
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": search_request}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_model_1")

        search_request = "not_exist_model"
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": search_request}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "")

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="test_name1", country="test_country1")
        Manufacturer.objects.create(name="test_name2", country="test_country2")

        search_request = "test_name1"
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": search_request}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_name1")

        search_request = "not_exist_name"
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": search_request}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "")
