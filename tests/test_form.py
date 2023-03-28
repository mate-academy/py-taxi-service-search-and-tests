from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver
from taxi.forms import (
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
)


class TestCarSearchForm(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        self.car1 = Car.objects.create(
            model="car1_test", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="car2_test", manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="CAR1_test", manufacturer=self.manufacturer
        )

    def test_search_car_by_model(self):
        form_data = {"model": "car1"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        queryset = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )

        self.assertIn(self.car1, queryset)
        self.assertNotIn(self.car2, queryset)
        self.assertIn(self.car3, queryset)


class TestDriverSearchForm(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(
            username="test_driver1",
            first_name="test_first_name1",
            last_name="test_last_name1",
            password="test_password1",
            license_number="BAC12345",
        )
        self.driver2 = Driver.objects.create(
            username="test_driver2",
            first_name="test_first_name2",
            last_name="test_last_name2",
            password="test_password2",
            license_number="BBC12345",
        )

    def test_search_driver_by_username(self):
        form_data = {"username": "driver1"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        queryset = get_user_model().objects.filter(
            username__icontains=form.cleaned_data["username"]
        )

        self.assertIn(self.driver1, queryset)
        self.assertNotIn(self.driver2, queryset)


class TestDriverCreationForm(TestCase):
    def test_create_driver_with_valid_data(self):
        form_data = {
            "username": "test_driver",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password12",
            "password2": "test_password12",
            "license_number": "BAC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_driver_with_lowercase_in_license(self):
        form_data = {
            "username": "test_driver",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password12",
            "password2": "test_password12",
            "license_number": "bac12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_driver_without_letters_in_license(self):
        form_data = {
            "username": "test_driver",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password12",
            "password2": "test_password12",
            "license_number": "32112345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_driver_with_1_symbol_in_license(self):
        form_data = {
            "username": "test_driver",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test_password12",
            "password2": "test_password12",
            "license_number": "1",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestDriverLicenseUpdateForm(TestCase):
    def test_update_driver_license_with_valid_data(self):
        form_data = {"license_number": "BAC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_driver_license_with_lowercase(self):
        form_data = {"license_number": "bac12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    """without letters or with another number of symbols by analogy"""
