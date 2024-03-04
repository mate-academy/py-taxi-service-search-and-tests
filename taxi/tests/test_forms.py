from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car

from taxi.forms import (
    validate_license_number,
    DriverLicenseUpdateForm,
    DriverCreationForm,
)

from taxi.models import Driver


class FormsTests(TestCase):
    def test_driver_creation_form_with_custom_fields(self):
        form_data = {
            "username": "new_driver",
            "password1": "driver123test",
            "password2": "driver123test",
            "first_name": "Name first",
            "last_name": "Name last",
            "license_number": "ADM56984"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):
        form_data = {
            "license_number": "WGM56484",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class TestsValidLicenseNumber(TestCase):
    @staticmethod
    def create_form(license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": license_number}
        )

    def test_license_number_should_be_8(self):
        self.assertFalse(self.create_form("ADM569844").is_valid())
        self.assertFalse(self.create_form("ADM5698").is_valid())

    def test_first_3_uppercase_letters(self):
        self.assertFalse(self.create_form("AD356983").is_valid())
        self.assertFalse(self.create_form("1DM56983").is_valid())
        self.assertFalse(self.create_form("E2M56983").is_valid())

    def test_last_5_characters_should_be_be_digits(self):
        self.assertFalse(self.create_form("ADMA6983").is_valid())
        self.assertFalse(self.create_form("ADM1d983").is_valid())
        self.assertFalse(self.create_form("ADM12d83").is_valid())
        self.assertFalse(self.create_form("ADM123d3").is_valid())
        self.assertFalse(self.create_form("ADM1298d").is_valid())


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Volvo"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="Volvo")),
        )

    def test_search_drivers_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?name=test"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="test")),
        )

    def test_search_cars_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?name=7")
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="7")),
        )
