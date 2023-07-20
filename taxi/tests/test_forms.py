from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer
from taxi.forms import DriverCreationForm, ManufacturerSearchForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_names_is_valid(self):

        form_data = {
            "username": "new_driver",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password"
        )
        self.client.force_login(self.user)

    def test_create_author(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class ManufacturerSearchFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Tesla")
        Manufacturer.objects.create(name="Honda")

    def test_valid_search(self):
        url = reverse("taxi:manufacturer-list")

        response = self.client.get(url, {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "form")
        self.assertContains(response, 'value="Toyota"')

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")
        self.assertNotContains(response, "Honda")

    def test_blank_search(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": ""})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "form")

        self.assertContains(response, "Toyota")
        self.assertContains(response, "Tesla")
        self.assertContains(response, "Honda")

    def test_invalid_search(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "InvalidManufacturer"})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "form")
        self.assertContains(response, 'value="InvalidManufacturer"')

        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")
        self.assertNotContains(response, "Honda")
