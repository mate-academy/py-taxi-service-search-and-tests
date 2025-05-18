from django.test import TestCase
from .models import Driver, Car, Manufacturer
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.forms import (
    DriverCreationForm,
)


class DriverModelTest(TestCase):
    def test_str_method(self):
        driver = Driver(
            username="testuser",
            first_name="Test",
            last_name="User"
        )
        self.assertEqual(str(driver), "testuser (Test User)")

    def test_get_absolute_url(self):
        driver = Driver(
            username="testuser",
            first_name="Test",
            last_name="User"
        )
        driver.pk = 1
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_license_number_unique(self):
        driver1 = Driver(
            username="testuser1",
            first_name="Test",
            last_name="User",
            license_number="ABC12345"
        )
        driver2 = Driver(
            username="testuser2",
            first_name="Test",
            last_name="User",
            license_number="ABC12345"
        )

        driver1.save()

        with self.assertRaises(IntegrityError):
            driver2.save()


class CarModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer(
            name="Toyota",
            country="Japan"
        )
        manufacturer.save()  # Save the manufacturer first
        car = Car(
            model="Corolla",
            manufacturer=manufacturer
        )
        # Assuming __str__ method returns model name
        self.assertEqual(str(car), "Corolla")


class ManufacturerModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.url = reverse("taxi:manufacturer-list")

    def test_list_view_status_code(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_list_view_context(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, "Toyota")

    def test_list_view_template(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")

    def test_list_view_pagination(self):
        for i in range(10):
            Manufacturer.objects.create(
                name=f"Manufacturer {i}",
                country="Country"
            )

        resp = self.client.get(self.url)
        self.assertEqual(len(resp.context["manufacturer_list"]), 5)


class DriverCreationFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "testuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User",
        }
        self.form = DriverCreationForm(data=self.form_data)

    def test_form_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_form_save(self):
        if self.form.is_valid():
            driver = self.form.save()
            self.assertEqual(driver.username, "testuser")
            self.assertEqual(driver.first_name, "Test")
            self.assertEqual(driver.last_name, "User")
            self.assertEqual(driver.license_number, "ABC12345")
            self.assertTrue(driver.check_password("StrongPass123!"))

    def test_invalid_form(self):
        self.form_data["license_number"] = "INVALID"
        form = DriverCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
