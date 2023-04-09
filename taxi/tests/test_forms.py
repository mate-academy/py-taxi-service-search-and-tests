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
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.driver1 = Driver.objects.create_user(
            username="driver1",
            password="testpass123",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="testpass123",
            license_number="ABD12345"
        )

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

    def test_form_invalid_blank_license_number(self):
        driver = Driver.objects.create(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            license_number="ABC12345",
        )
        data = {"license_number": ""}
        form = DriverLicenseUpdateForm(instance=driver, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["license_number"], ["This field is required."])

    def test_form_invalid_license_number_format(self):
        driver = Driver.objects.create(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            license_number="ABC12345",
        )
        data = {"license_number": "12345678"}
        form = DriverLicenseUpdateForm(instance=driver, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"], ["First 3 characters should be uppercase letters."]
        )

    def test_form_invalid_duplicate_license_number(self):
        driver1 = Driver.objects.create(
            username="testuser1",
            password="testpassword",
            email="testuser1@example.com",
            license_number="ABC12345",
        )
        driver2 = Driver.objects.create(
            username="testuser2",
            password="testpassword",
            email="testuser2@example.com",
            license_number="DEF67890",
        )
        data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(instance=driver2, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["license_number"], ["Driver with this License number already exists."]
        )
