from django.contrib.auth import get_user_model
from django.test import TestCase
from django import forms
from django.test.client import RequestFactory
from django.urls import reverse

from taxi.forms import (
    ManufacturerNameSearchForm,
    CarForm,
    CarModelSearchForm,
    DriverUsernameSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm
)
from taxi.models import Car, Manufacturer, Driver


class SearchFormsTest(TestCase):
    def test_manufacturer_form_fields(self):
        form = ManufacturerNameSearchForm()
        self.assertTrue(isinstance(form.fields["name"], forms.CharField))

    def test_manufacturer_form_label(self):
        form = ManufacturerNameSearchForm()
        self.assertEqual(form.fields["name"].label, "")

    def test_manufacturer_form_widgets(self):
        form = ManufacturerNameSearchForm()
        widget_attrs = form.fields["name"].widget.attrs
        self.assertEqual(widget_attrs["placeholder"], "Search by name...")

    def test_manufacturer_valid_form(self):
        form = ManufacturerNameSearchForm(data={"name": "Test Manufacturer"})
        self.assertTrue(form.is_valid())


class CarFormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test1",
            country="TestCountry1"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )

    def test_car_form_valid(self):
        manufacturer2 = Manufacturer.objects.create(
            name="test1=2",
            country="TestCountry2"
        )
        data = {
            "model": "Test Model 2",
            "manufacturer": manufacturer2,
            "drivers": [self.user.id],
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        data = {
            "model": "",
            "manufacturer": "Test Manufacturer",
            "drivers": [self.user.id],
        }
        form = CarForm(data=data)
        self.assertFalse(form.is_valid())

    def test_car_form_save(self):
        manufacturer2 = Manufacturer.objects.create(
            name="test1=2",
            country="TestCountry2"
        )
        data = {
            "model": "Test Model 3",
            "manufacturer": manufacturer2,
            "drivers": [self.user.id],
        }
        request = self.factory.post(reverse("taxi:car-create"), data=data)
        request.user = self.user
        form = CarForm(data=data)
        if form.is_valid():
            car = form.save(commit=False)
            car.save()

        self.assertTrue(Car.objects.filter(model="Test Model 3").exists())


class CarSearchFormTest(TestCase):
    def test_car_form_fields(self):
        form = CarModelSearchForm()
        self.assertTrue(isinstance(form.fields["model"], forms.CharField))

    def test_car_form_label(self):
        form = CarModelSearchForm()
        self.assertEqual(form.fields["model"].label, "")

    def test_car_form_widgets(self):
        form = CarModelSearchForm()
        widget_attrs = form.fields["model"].widget.attrs
        self.assertEqual(widget_attrs["placeholder"], "Search by model...")

    def test_car_valid_form(self):
        form = CarModelSearchForm(data={"model": "Test model"})
        self.assertTrue(form.is_valid())


class DriverSearchFormTest(TestCase):
    def test_driver_form_fields(self):
        form = DriverUsernameSearchForm()
        self.assertTrue(isinstance(form.fields["username"], forms.CharField))

    def test_driver_form_label(self):
        form = DriverUsernameSearchForm()
        self.assertEqual(form.fields["username"].label, "")

    def test_driver_form_widgets(self):
        form = DriverUsernameSearchForm()
        widget_attrs = form.fields["username"].widget.attrs
        self.assertEqual(widget_attrs["placeholder"], "Search by username...")

    def test_driver_valid_form(self):
        form = DriverUsernameSearchForm(data={"username": "Test username"})
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password"
        )

    def test_driver_creation_form_valid(self):
        data = {
            "username": "test_driver",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "TES12345",
            "first_name": "Test",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid(self):
        data = {
            "username": "test_driver",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "InvalidLicenseNumber",
            "first_name": "Test",
            "last_name": "Driver",
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_save(self):
        data = {
            "username": "test_driver",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "TES12345",
            "first_name": "Test",
            "last_name": "Driver",
        }
        request = self.factory.post(reverse("taxi:driver-create"), data=data)
        request.user = self.user
        form = DriverCreationForm(data=data)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.save()

        self.assertTrue(Driver.objects.filter(username="test_driver").exists())


class DriverLicenseUpdateFormTest(TestCase):

    def test_valid_license_number(self):
        data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_length_license_number(self):
        data = {"license_number": "ABC1234"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

    def test_invalid_case_license_number(self):
        data = {"license_number": "ABc12345"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

    def test_invalid_format_license_number(self):
        data = {"license_number": "ABC1XYZ5"}
        form = DriverLicenseUpdateForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )
