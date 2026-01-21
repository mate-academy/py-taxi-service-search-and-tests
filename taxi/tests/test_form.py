from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (CarForm, CarModelSearchForm,
                        DriverCreationForm, ManufacturerNameSearchForm)
from taxi.models import Manufacturer, Driver


class CarFormsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer", country="TestCountry"
        )
        self.driver1 = Driver.objects.create_user(
            username="driver1",
            password="password123",
            license_number="QWE12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="password123",
            license_number="EWQ67890"
        )

    def test_car_form_valid(self):
        data = {
            "model": "TestModel",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk],
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid())

    def test_car_form_save(self):
        data = {
            "model": "TestModel",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk],
        }
        form = CarForm(data=data)
        if form.is_valid():
            car = form.save()
            self.assertEqual(car.model, data["model"])
            self.assertEqual(car.manufacturer, self.manufacturer)
            self.assertIn(self.driver1, car.drivers.all())
            self.assertIn(self.driver2, car.drivers.all())
        else:
            self.fail("This form invalid")

    def test_car_form_invalid(self):
        data = {
            "model": "",
            "manufacturer": self.manufacturer.pk,
        }
        form = CarForm(data=data)
        self.assertFalse(form.is_valid())

    def test_search_form_field_placeholder(self):
        form = CarModelSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model"
        )

    def test_search_form_model_field_valid_input(self):
        form = CarModelSearchForm(data={"model": "Toyota"})
        self.assertTrue(form.is_valid())


class DriverFormsTests(TestCase):
    def test_driver_creation_with_license_first_name_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "SSD12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
        self.assertEqual(form.cleaned_data.get("license_number"), "SSD12345")


class PrivateAuthorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test_first",
            "last_name": "Test_last",
            "license_number": "SSD12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class ManufacturerSearchFormTests(TestCase):
    def test_form_valid_with_valid_data(self):
        form_data = {"name": "Toyota"}
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")

    def test_search_form_field_placeholder(self):
        form = ManufacturerNameSearchForm()
        widget = form.fields["name"].widget
        self.assertEqual(widget.attrs["placeholder"], "Search by name")
