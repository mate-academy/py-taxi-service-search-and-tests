from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    CarSearchForm
)
from taxi.models import Manufacturer, Driver, Car


class FormTests(TestCase):
    def test_driver_creation_form_with_all_fields_is_valid(
            self
    ) -> None:
        form_data = {
            "username": "username",
            "password1": "123password321",
            "password2": "123password321",
            "license_number": "ABC12345",
            "first_name": "first_name",
            "last_name": "last_name",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_with_field_is_valid(self) -> None:
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_format(self) -> None:
        valid_license_numbers = [
            "ABC12345", "XYZ67890",
        ]
        invalid_license_numbers = [
            "AB12345",
            "ABCD123456",
            "abc12345",
            "ABc12345",
            "ABC12abc",
            "ABC1234A",
        ]

        for license_number in valid_license_numbers:
            form_data = {
                "username": "username",
                "password1": "123password321",
                "password2": "123password321",
                "license_number": license_number,
                "first_name": "first_name",
                "last_name": "last_name",
            }
            form = DriverCreationForm(data=form_data)
            self.assertTrue(form.is_valid())

        for license_number in invalid_license_numbers:
            form_data = {
                "username": "username",
                "password1": "123password321",
                "password2": "123password321",
                "license_number": license_number,
                "first_name": "first_name",
                "last_name": "last_name",
            }
            form = DriverCreationForm(data=form_data)
            self.assertFalse(form.is_valid())


class SearchFunctionalityTests(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(username="John Doe")
        self.driver2 = Driver.objects.create(username="Jane Doe")

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.manufacturer2 = Manufacturer.objects.create(name="Honda")

        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Accord",
            manufacturer=self.manufacturer2
        )

    def test_driver_search_functionality(self):
        form_data = {"username": "John Doe"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        search_result = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0], self.driver1)

    def test_manufacturer_search_functionality(self):
        form_data = {"name': 'Toyota"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        search_result = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0], self.manufacturer1)

    def test_car_search_functionality(self):
        form_data = {"model": "Camry"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        search_result = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0], self.car2)
