from django.test import TestCase
from taxi.models import Driver, Manufacturer
from taxi.forms import (CarForm,
                        DriverCreationForm,
                        DriverLicenseUpdateForm,
                        DriverSearchForm,
                        CarSearchForm,
                        ManufacturerSearchForm)


class TestCarForm(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        self.driver1 = Driver.objects.create_user(username="driver1", password="testpass123", license_number="ABC12345")
        self.driver2 = Driver.objects.create_user(username="driver2", password="testpass123", license_number="ABD12345")

        self.valid_data = {
            "model": "Test Model",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk],
        }

    def test_car_form_valid(self):
        form = CarForm(data=self.valid_data)
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_form_valid(self):
        data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))
        self.assertIsInstance(user, Driver)
        self.assertEqual(user.license_number, "ABC12345")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")


class DriverLicenseUpdateFormTest(TestCase):
    def test_form_valid(self):
        driver = Driver.objects.create(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            license_number="ABC12345",
        )
        data = {"license_number": "DEF67890"}
        form = DriverLicenseUpdateForm(instance=driver, data=data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.license_number, "DEF67890")


class DriverSearchFormTest(TestCase):
    def test_form_valid(self):
        data = {"username": "testuser"}
        form = DriverSearchForm(data=data)
        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_form_valid(self):
        data = {"model": "Test Car"}
        form = CarSearchForm(data=data)
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_form_valid(self):
        data = {"name": "Test Manufacturer"}
        form = ManufacturerSearchForm(data=data)
        self.assertTrue(form.is_valid())
