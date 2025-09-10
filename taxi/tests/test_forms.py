from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    CarsModelSearchForm,
    ManufacturerNameSearchForm,
    DriverUsernameSearchForm
)
from taxi.models import Driver, Manufacturer


class DriverCreationFormTests(TestCase):
    def test_valid_form(self):
        data = {
            "username": "new_driver",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "test"
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.username, "new_driver")
        self.assertEqual(driver.license_number, "ABC12345")

    def test_invalid_license_number(self):
        data = {
            "username": "new_driver2",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "123",
            "first_name": "Test",
            "last_name": "Test"
        }
        form = DriverCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="pass12345",
            license_number="ABC12345"
        )

    def test_valid_license_update(self):
        form = DriverLicenseUpdateForm(
            instance=self.driver,
            data={"license_number": "DEF67890"}
        )
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.license_number, "DEF67890")

    def test_invalid_license_update(self):
        form = DriverLicenseUpdateForm(
            instance=self.driver,
            data={"license_number": "ABC"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="USA"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="pass",
            license_number="AAA11111"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="pass",
            license_number="BBB22222"
        )

    def test_car_form_valid(self):
        data = {
            "model": "Model X",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk]
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid())
        car = form.save()
        self.assertEqual(car.model, "Model X")
        self.assertEqual(
            list(car.drivers.all()),
            [self.driver1, self.driver2]
        )


class SearchFormsTests(TestCase):
    def test_car_model_search_form_valid(self):
        form = CarsModelSearchForm(data={"model": "Model X"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_name_search_form_valid(self):
        form = ManufacturerNameSearchForm(data={"name": "Tesla"})
        self.assertTrue(form.is_valid())

    def test_driver_username_search_form_valid(self):
        form = DriverUsernameSearchForm(data={"username": "driver1"})
        self.assertTrue(form.is_valid())
