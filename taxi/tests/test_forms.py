from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class DriverFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test password"
        )
        self.client.force_login(self.user)

    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "test_user1",
            "first_name": "Test first",
            "last_name": "Test last",
            "password1": "Test password123",
            "password2": "Test password123",
            "license_number": "PAY56789",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_update_license_number_8_characters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABS1234"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

    def test_update_license_number_3_characters_uppercase_letters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "Abs12345"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

    def test_update_license_number_5_last_characters_digits(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABS123df"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )


class CarFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Test Manufacturer1")
        Manufacturer.objects.create(name="Test Manufacturer2")
        get_user_model().objects.create_user(
            username="Test_1!",
            password="test password123",
            license_number="QAS12345"
        )
        get_user_model().objects.create_user(
            username="Test_2!",
            password="test password123",
            license_number="TER12345"
        )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test password"
        )
        self.client.force_login(self.user)

    def test_template_car_form(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_car_form_checkbox_select_multiple_widget(self):
        response = self.client.get(reverse("taxi:car-create"))
        form = response.context["form"]
        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple
        )

    def test_driver_search_form_placeholder(self):
        response = self.client.get(reverse("taxi:driver-list"))
        form = response.context["form"]
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username.."
        )

    def test_manufacturer_search_form_placeholder(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        form = response.context["form"]
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name.."
        )

    def test_car_search_form_placeholder(self):
        response = self.client.get(reverse("taxi:car-list"))
        form = response.context["form"]
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model.."
        )
