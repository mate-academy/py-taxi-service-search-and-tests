from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    validate_license_number,
)
from taxi.models import Driver, Car, Manufacturer


class DriverTests(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "NUM12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_number_update(self):
        new_license = "COL54321"
        driver_ = get_user_model().objects.create_user(
            username="Colin",
            password="colin12345",
            license_number="COL12345"
        )
        self.client.force_login(driver_)
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": driver_.id}),
            {
                "license_number": new_license
            },
        )
        get_user_model().objects.get(id=driver_.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            get_user_model().objects.get(id=driver_.id).license_number,
            new_license
        )


class LicenseNumberValidationTest(TestCase):
    def test_correct_license_number(self):
        license_number_ = "NUM12345"

        self.assertEqual(
            license_number_,
            validate_license_number(license_number_)
        )

    def test_wrong_length_license_number(self):
        short_number = "NUM123"
        long_number = "NUM12345678"
        message = "License number should consist of 8 characters"

        with self.assertRaisesMessage(
            ValidationError,
            message
        ):
            validate_license_number(short_number)
            validate_license_number(long_number)

    def test_first_3_uppercase_letters(self):
        lowercase = "num12345"
        not_alpha = "12345678"
        message = "First 3 characters should be uppercase letters"

        with self.assertRaisesMessage(
            ValidationError,
            message
        ):
            validate_license_number(lowercase)
            validate_license_number(not_alpha)

    def test_last_5_characters_are_digits(self):
        not_digits = "NUMBER12"
        message = "Last 5 characters should be digits"

        with self.assertRaisesMessage(
            ValidationError,
            message
        ):
            validate_license_number(not_digits)


class SearchFormsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345user",
            license_number="NUM12345"
        )
        self.client.force_login(self.user)

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?name=test"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="test"))
        )

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        Car.objects.create(
            model="Test model",
            manufacturer=(Manufacturer.objects.get(id=manufacturer.id))
        )
        response = self.client.get(
            reverse("taxi:car-list") + "?name=Test"
        )
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="Test"))
        )

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(
            name="test name",
            country="test country"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=test"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="test"))
        )
