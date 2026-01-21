from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number, DriverCreationForm
from taxi.models import Manufacturer, Car, Driver
from django.contrib.auth import get_user_model


class CustomLogicTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer2
        )

        self.driver1 = Driver.objects.create_user(
            username="driver1", password="pass123", license_number="QWE12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2", password="pass123", license_number="ZXC12345"
        )

    def test_license_number_validation_valid(self):
        valid = validate_license_number("ABC12345")
        self.assertEqual(valid, "ABC12345")

    def test_license_number_validation_invalid_format(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_toggle_assign_adds_car_to_driver(self):
        self.client.force_login(self.driver1)
        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car1.id]))
        self.assertIn(self.car1, self.driver1.cars.all())

    def test_toggle_assign_removes_car_from_driver(self):
        self.driver1.cars.add(self.car1)
        self.client.force_login(self.driver1)
        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car1.id]))
        self.assertNotIn(self.car1, self.driver1.cars.all())

    def test_driver_creation_form_creates_driver(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "ABC12345",
            "first_name": "Alex",
            "last_name": "Smith",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.username, "newdriver")
        self.assertTrue(driver.check_password("StrongPass123"))
        self.assertEqual(driver.license_number, "ABC12345")
        self.assertEqual(driver.first_name, "Alex")
        self.assertEqual(driver.last_name, "Smith")
