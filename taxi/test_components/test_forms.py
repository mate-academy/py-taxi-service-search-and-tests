from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    CarSearchForm,
    DriverSearchForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm
)


class FormsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="5 Series",
            manufacturer=self.manufacturer,
        )
        self.driver = Driver.objects.create(
            username="Test1",
            password="12345",
            license_number="ABC12345"
        )

    def test_car_creation(self):
        form_data = {
            "model": "3 Series",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], form_data["model"])
        self.assertEqual(
            form.cleaned_data["manufacturer"].id,
            form_data["manufacturer"]
        )
        self.assertEqual(list(form.cleaned_data["drivers"]), [self.driver])

    def test_drivers_widget(self):
        form = CarForm()
        widget = form.fields["drivers"].widget
        self.assertTrue(isinstance(widget, forms.CheckboxSelectMultiple))

    def test_driver_creation(self):
        form_data = {
            "username": "Username202",
            "password1": "WhatWasThat2024",
            "password2": "WhatWasThat2024",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ADC12349"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_not_valid_license_number_in_driver_creation(self):
        form_data = {
            "username": "Username202",
            "password1": "WhatWasThat2024",
            "password2": "WhatWasThat2024",
            "license_number": "AC1239"
        }
        form = DriverCreationForm(data=form_data)
        form.full_clean()
        self.assertTrue(not form.is_valid())

    def test_driver_update(self):
        form_data = {
            "license_number": "ACD12395"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_not_valid_license_number_in_driver_update(self):
        form_data = {
            "license_number": "AC1239"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        form.full_clean()
        self.assertTrue(not form.is_valid())
