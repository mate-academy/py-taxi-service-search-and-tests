from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturersSearchForm,
    CarForm
)
from taxi.models import Manufacturer


class DriverCreationFormTests(TestCase):
    def test_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_license(self):
        form_data = {
            "username": "newdriver",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "license_number": "abc",  # некорректный формат
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def test_valid_license(self):
        form = DriverLicenseUpdateForm(data={"license_number": "XYZ54321"})
        self.assertTrue(form.is_valid())

    def test_invalid_license(self):
        form = DriverLicenseUpdateForm(data={"license_number": "123"})
        self.assertFalse(form.is_valid())


class DriverSearchFormTests(TestCase):
    def test_cleaned_data(self):
        form = DriverSearchForm(data={"title": "user"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "user")


class CarSearchFormTests(TestCase):
    def test_cleaned_data(self):
        form = CarSearchForm(data={"title": "bmw"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "bmw")


class ManufacturersSearchFormTests(TestCase):
    def test_cleaned_data(self):
        form = ManufacturersSearchForm(data={"title": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Toyota")


class CarFormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="d1", license_number="ABC12345", password="test"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="d2", license_number="XYZ67890", password="test"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "X5",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertIn(self.driver1, form.cleaned_data["drivers"])
