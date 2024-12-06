from django.test import TestCase
from django.urls import reverse_lazy

from taxi.forms import DriverCreationForm


class DriverCreationFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_user",
            "password1": "gfdfd53g",
            "password2": "differentPass456",
            "first_name": "Andrew",
            "last_name": "Smith",
            "license_number": "XYZ98765",
        }

    def test_user_creation_form_with_valid_data(self):
        form_data = self.form_data
        form_data["password2"] = "gfdfd53g"
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(
            form.cleaned_data["first_name"], form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"], form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"], form_data["license_number"]
        )

    def test_user_creation_form_with_invalid_passwords(self):
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class SearchTests(TestCase):
    def setUp(self):
        self.data = {
            "model": "test_data",
            "page": 1,
        }

    def test_driver_search(self):
        data = self.data
        response = self.client.get(
            reverse_lazy("taxi:driver-list"), data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username")
        self.assertContains(response, "page")

    def test_car_search(self):
        data = self.data
        response = self.client.get(
            reverse_lazy("taxi:car-list"), data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "model")
        self.assertContains(response, "page")

    def test_manufacturer_search(self):
        data = self.data
        response = self.client.get(
            reverse_lazy("taxi:manufacturer-list"), data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")
        self.assertContains(response, "page")
