from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Driver


class CarFormTest(TestCase):
    def setUp(self):
        """Створюємо тестові дані для перевірки форми"""
        self.manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.driver = get_user_model().objects.create_user(username="testdriver", password="password123")

    def test_car_form_valid(self):
        """Перевіряємо, що форма CarForm валідна з правильними даними"""
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        form = CarForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        """Перевіряємо створення водія через форму"""
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "XYZ56789",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class DriverLicenseUpdateFormTest(TestCase):
    def test_driver_license_update_form_valid(self):
        """Перевіряємо оновлення ліцензії водія"""
        form = DriverLicenseUpdateForm(data={"license_number": "AAA11111"})
        self.assertTrue(form.is_valid())
