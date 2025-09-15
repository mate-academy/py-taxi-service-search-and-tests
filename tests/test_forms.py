from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm, CarForm,
                        DriverSearchForm, CarSearchForm,
                        ManufacturerSearchForm)
from taxi.models import Manufacturer, Car


class DriverCreationFormTest(TestCase):
    def test_valid_driver_creation_form(self):
        form_data = {
            "username": "User",
            "password1": "Test Password",
            "password2": "Test Password",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "ALI12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_invalid_license_number(self):
        form_data = {
            "username": "User",
            "password1": "Test Password",
            "password2": "Test Password",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "Aii12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_valid_license_update_form(self):
        form_data = {
            "license_number": "ALI12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"],
                         form_data["license_number"])

    def test_update_license_number(self):
        driver = get_user_model().objects.create_user(
            username="User",
            password="User123",
            license_number="ALI12345",
        )
        self.client.login(username="User", password="User123")
        response = self.client.post(reverse(
            "taxi:driver-update",
            args=[driver.id]),
            {
                "license_number": "VOV12345",
        })
        self.assertRedirects(response, reverse("taxi:driver-list"))
        driver.refresh_from_db()
        self.assertEqual(driver.license_number, "VOV12345")


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="UA",
        )
        self.driver1 = get_user_model().objects.create_user(
            username="Volodymyr",
            password="Test Password",
            license_number="VOV12345",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="Alina",
            password="Test Password",
            license_number="ALI12345",
        )

    def test_valid_car_form(self):
        form_data = {
            "model": "Test Model",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

        car = form.save()
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(car.model, "Test Model")
        self.assertIn(self.driver1, car.drivers.all())
        self.assertIn(self.driver2, car.drivers.all())

    def test_invalid_car_form_missing_model(self):
        form_data = {
            "model": "",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)


class SearchFormTest(TestCase):
    def test_driver_search_empty_and_filled(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

        form = DriverSearchForm(data={"username": "Alina"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "Alina")

    def test_car_search_empty_and_filled(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

        form = CarSearchForm(data={"model": "Mazda"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Mazda")

    def test_manufacturer_search_empty_and_filled(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

        form = ManufacturerSearchForm(data={"name": "Mitsubishi"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Mitsubishi")
