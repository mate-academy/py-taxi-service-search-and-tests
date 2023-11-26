from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.forms import (
    DriverCreationForm,
    CarForm,
    DriverLicenseUpdateForm,
    DriverUsernameSearchForm,
    CarModelSearchForm,
    ManufacturerNameSearchForm,
)
from taxi.models import Driver, Car, Manufacturer


class FormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Object",
        )

        cls.user = get_user_model().objects.create_user(
            username="secondtestsuser",
            password="test123",
            license_number="ABC54321",
        )

        cls.car = Car.objects.create(
            model="ClassCar",
            manufacturer=cls.manufacturer,
        )

    def test_car_form(self):
        form_data = {
            "model": "TestCar",
            "manufacturer": self.manufacturer,
            "drivers": get_user_model().objects.filter(pk=1),
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], form_data["model"])
        self.assertEqual(
            form.cleaned_data["manufacturer"],
            form_data["manufacturer"],
        )
        self.assertEqual(
            list(form.cleaned_data["drivers"]),
            list(form_data["drivers"]),
        )

    def test_driver_creation_form_with_license_number_is_valid(self):
        form_data = {
            "username": "new_user",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User",
            "password1": "user123test",
            "password2": "user123test",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form(self):
        form_data = {
            "license_number": "li32",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data["license_number"] = "BCD32114"
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_username_search_form(self):
        form_data = {
            "username": "secondtestsuser",
        }
        form = DriverUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_model_search_form(self):
        form_data = {
            "model": "ClassCar",
        }
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_name_search_form(self):
        form_data = {
            "name": "Test",
        }
        form = ManufacturerNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
