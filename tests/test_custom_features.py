from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Driver, Manufacturer, Car


class LicenseNumberValidationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_valid_license_number(self):
        form_data = {
            "username": "testDriver",
            "license_number": "ABC12345",
            "first_name": "Test First",
            "last_name": "Test Last",
            "password1": "3edczaq1",
            "password2": "3edczaq1",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_license_number_lowercase(self):
        form_data = {
            "username": "test",
            "license_number": "abc12345",
            "first_name": "Test First",
            "last_name": "Test Last",
            "password1": "3edczaq1",
            "password2": "3edczaq1",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_license_number_without_fulfilling(self):
        form_data = {
            "username": "test",
            "license_number": "KA7993IA",
            "first_name": "Test First",
            "last_name": "Test Last",
            "password1": "3edczaq1",
            "password2": "3edczaq1",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_assign_car(self):
        driver = Driver.objects.create(
            username="Test Driver",
            license_number="ABC12345",
            first_name="Test Driver First",
            last_name="Test Driver Last",
        )
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        car = Car.objects.create(
            model="Test Car",
            manufacturer=manufacturer
        )
        self.client.force_login(driver)

        response = self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                args=[car.id]
            )
        )
        self.assertEqual(response.status_code, 302)
        driver.refresh_from_db()
        self.assertIn(car, driver.cars.all())

        response = self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                args=[car.id]
            )
        )
        self.assertEqual(response.status_code, 302)
        driver.refresh_from_db()
        self.assertNotIn(car, driver.cars.all())
