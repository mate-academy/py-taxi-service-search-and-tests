from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import Manufacturer, Car, Driver


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number_first_last_name_is_valid(
        self,
    ):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "AOU12345",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenseUpdateFormTestCase(TestCase):
    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())

    def test_invalid_license_number_length(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABCD123"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"],
        )

    def test_invalid_license_number_format(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"],
        )

        form = DriverLicenseUpdateForm(data={"license_number": "ABC12X45"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"],
        )


class CarFormTestCase(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="testdriver1",
            password="test_password",
            license_number="DCF12345",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="testdriver2",
            password="test_password",
            license_number="YUI12345",
        )

    def test_valid_car_form(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        form_data = {
            "manufacturer": manufacturer,
            "model": "Camry",
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        print(form.errors)

    def test_car_form_without_drivers_is_invalid(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        form_data = {
            "manufacturer": manufacturer,
            "model": "Camry",
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)

    def test_car_form_with_invalid_drivers_is_invalid(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        invalid_driver_id = 999
        form_data = {
            "manufacturer": manufacturer,
            "model": "Camry",
            "drivers": [self.driver1.id, invalid_driver_id],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)


class SearchFormTestCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="test@test"
        )
        self.client.force_login(self.user)

        # create test objects
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford", country="USA"
        )
        self.driver1 = Driver.objects.create_user(
            username="driver1", password="test@test", license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2", password="test@test", license_number="XYZ78901"
        )
        self.car1 = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer1
        )
        self.car1.drivers.add(self.driver1)
        self.car2 = Car.objects.create(
            model="Mustang", manufacturer=self.manufacturer2
        )
        self.car2.drivers.add(self.driver2)

    def test_search_car(self):
        search_info = "Mustang"
        response = self.client.get(f"/cars/?model={search_info}")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains=search_info),
        )

    def test_search_driver(self):
        search_info = "driver1"
        response = self.client.get(f"/drivers/?username={search_info}")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            Driver.objects.filter(username__icontains=search_info),
        )

    def test_search_manufacturer(self):
        search_info = "Ford"
        response = self.client.get(f"/manufacturers/?name={search_info}")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains=search_info),
        )
