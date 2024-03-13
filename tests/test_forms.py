from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer
from taxi.forms import (CarForm,
                        CarSearchForm,
                        DriverCreationForm,
                        DriverLicenseUpdateForm,
                        DriverSearchForm,
                        ManufacturerSearchForm)


class CarFormTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.driver = Driver.objects.create(
            username="test_driver_1",
            password="pass1234", license_number="TES12345")

    def test_car_form_valid(self) -> None:
        form = CarForm(
            data={"model": "Test Model",
                  "manufacturer": self.manufacturer.id,
                  "drivers": [self.driver.id]}
        )
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.driver = Driver.objects.create(
            username="test_driver_1",
            password="pass1234",
            license_number="TES12345"
        )
        self.car1 = Car.objects.create(
            model="Test Model 1",
            manufacturer=self.manufacturer
        )
        self.car1.drivers.add(self.driver)
        self.car2 = Car.objects.create(
            model="Test Model 2",
            manufacturer=self.manufacturer
        )
        self.car2.drivers.add(self.driver)
        self.car3 = Car.objects.create(
            model="Test Model 3",
            manufacturer=self.manufacturer
        )
        self.car3.drivers.add(self.driver)

    def test_car_search_form_search_logic(self):
        form = CarSearchForm(data={"model": "Test Model 1"})
        self.assertTrue(form.is_valid())
        search_results = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].model, "Test Model 1")


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form = DriverCreationForm(
            data={
                "username": "test_driver_1",
                "password1": "test12345",
                "password2": "test12345",
                "license_number": "TES12345",
                "first_name": "First",
                "last_name": "Last"})
        valid = form.is_valid()
        if not valid:
            print(form.errors)
        self.assertTrue(valid)


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TES12345"})
        self.assertTrue(form.is_valid())

    def test_license_number_length(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TES123456"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["License number should consist of 8 characters"]
        )

    def test_license_number_uppercase_letters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "tes12345"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["First 3 characters should be uppercase letters"]
        )

    def test_license_number_digits(self):
        form = DriverLicenseUpdateForm(data={"license_number": "TESABCDE"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"],
            ["Last 5 characters should be digits"]
        )


class DriverSearchFormTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(
            username="test_driver_1",
            password="pass1234",
            license_number="TES12345"
        )
        self.driver2 = Driver.objects.create(
            username="test_driver_2",
            password="pass1234",
            license_number="TES12346"
        )
        self.driver3 = Driver.objects.create(
            username="test_driver_3",
            password="pass1234",
            license_number="TES12347"
        )

    def test_driver_search_form_search_logic(self):
        form = DriverSearchForm(data={"username": "test_driver_1"})
        self.assertTrue(form.is_valid())

        search_results = Driver.objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].username, "test_driver_1")


class ManufacturerSearchFormTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test Manufacturer 1",
            country="Test Country 1"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Test Manufacturer 2",
            country="Test Country 2"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Test Manufacturer 3",
            country="Test Country 3"
        )

    def test_manufacturer_search_form_search_logic(self):
        form = ManufacturerSearchForm(data={"name": "Test Manufacturer 1"})
        self.assertTrue(form.is_valid())

        search_results = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].name, "Test Manufacturer 1")
