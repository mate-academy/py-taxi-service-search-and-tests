from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm)
from taxi.models import Driver, Car, Manufacturer


class DriverFormTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "username",
            "password1": "user12test",
            "password2": "user12test",
            "license_number": "ABC12345",
            "first_name": "user_first_name",
            "last_name": "user_last_name",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.data, form_data)

    def check_validate_errors(self, form_data, error_message):
        # form = DriverLicenseUpdateForm(data=form_data)
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"], [error_message])

    def test_license_number_is_too_short(self):
        form_data = {"license_number": "ABC1234"}
        error_message = "License number should consist of 8 characters"
        DriverFormTests.check_validate_errors(
            self,
            form_data=form_data,
            error_message=error_message
        )

    def test_license_number_is_too_long(self):
        form_data = {"license_number": "ABC123456"}
        error_message = "License number should consist of 8 characters"
        DriverFormTests.check_validate_errors(
            self,
            form_data=form_data,
            error_message=error_message
        )

    def test_license_number_dont_have_prefix_with_three_letters(self):
        form_data = {"license_number": "AB123456"}
        error_message = "First 3 characters should be uppercase letters"
        DriverFormTests.check_validate_errors(
            self,
            form_data=form_data,
            error_message=error_message
        )

    def test_license_number_dont_have_prefix_with_three_uppercase(self):
        form_data = {"license_number": "abc12345"}
        error_message = "First 3 characters should be uppercase letters"
        DriverFormTests.check_validate_errors(
            self,
            form_data=form_data,
            error_message=error_message
        )

    def test_license_number_dont_have_postfix_with_five_numbers(self):
        form_data = {"license_number": "ABCD2345"}
        error_message = "Last 5 characters should be digits"
        DriverFormTests.check_validate_errors(
            self,
            form_data=form_data,
            error_message=error_message
        )


class DriverSearchFormsTest(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="johnsmith",
            license_number="ABC12345",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="tylerderden",
            license_number="ABC12346",
        )
        self.driver3 = get_user_model().objects.create_user(
            username="tyleranderson",
            license_number="ABC12347",
        )

    def test_driver_search_form_single(self):
        form_data = {"username": "john"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertEqual(filtered_data.count(), 1)
        self.assertEqual(filtered_data.first(), self.driver1)

    def test_driver_search_form_two(self):
        form_data = {"username": "tyler"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertEqual(filtered_data.count(), 2)
        self.assertNotIn(self.driver1, filtered_data)
        self.assertIn(self.driver2, filtered_data)
        self.assertIn(self.driver3, filtered_data)

    def test_driver_search_form_not_exist(self):
        form_data = {"username": "nobody"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertEqual(filtered_data.count(), 0)

    def test_driver_search_form_empty(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertEqual(filtered_data.count(), 3)


class CarSearchFormsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacture",
            country="test_country"
        )
        self.car1 = Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer,
        )
        self.car2 = Car.objects.create(
            model="Ford",
            manufacturer=self.manufacturer,
        )
        self.car3 = Car.objects.create(
            model="Mitsubishi",
            manufacturer=self.manufacturer,
        )

    def test_car_search_form_single(self):
        form_data = {"model": "BMW"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertEqual(filtered_data.count(), 1)
        self.assertEqual(filtered_data.first(), self.car1)

    def test_car_search_form_two(self):
        form_data = {"model": "b"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertEqual(filtered_data.count(), 2)
        self.assertIn(self.car1, filtered_data)
        self.assertNotIn(self.car2, filtered_data)
        self.assertIn(self.car3, filtered_data)

    def test_car_search_form_not_exist(self):
        form_data = {"model": "nothing"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertEqual(filtered_data.count(), 0)

    def test_car_search_form_empty(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertEqual(filtered_data.count(), 3)


class ManufacturerSearchFormsTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="manufacturer1",
            country="test_country",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="manufacturerr2",
            country="test_country",
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="manufacturerr3",
            country="test_country",
        )

    def test_manufacturer_search_form_single(self):
        form_data = {"name": "manufacturer1"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertEqual(filtered_data.count(), 1)
        self.assertEqual(filtered_data.first(), self.manufacturer1)

    def test_manufacturer_search_form_two(self):
        form_data = {"name": "manufacturerr"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertEqual(filtered_data.count(), 2)
        self.assertNotIn(self.manufacturer1, filtered_data)
        self.assertIn(self.manufacturer2, filtered_data)
        self.assertIn(self.manufacturer3, filtered_data)

    def test_manufacturer_search_form_not_exist(self):
        form_data = {"name": "nothing"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertEqual(filtered_data.count(), 0)

    def test_manufacturer_search_form_empty(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        filtered_data = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertEqual(filtered_data.count(), 3)
