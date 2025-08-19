from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Manufacturer, Car

Driver = get_user_model()


class FormsTests(TestCase):
    def test_driver_creation_form_valid_data(self):
        form_data = {
            "username": "admin",
            "first_name": "admin_first_name",
            "last_name": "admin_last_name",
            "license_number": "ADM12345",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )
        self.assertEqual(
            form.cleaned_data["license_number"],
            form_data["license_number"]
        )
        self.assertEqual(
            form.cleaned_data["password1"],
            form_data["password1"]
        )

    def test_driver_creation_form_save_creates_driver(self):
        form_data = {
            "username": "admin2",
            "first_name": "admin2 first name",
            "last_name": "admin2 last name",
            "license_number": "AAA11111",
            "password1": "3edczaq1",
            "password2": "3edczaq1",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        driver = form.save()
        self.assertEqual(driver.username, "admin2")
        self.assertEqual(driver.first_name, "admin2 first name")
        self.assertEqual(driver.last_name, "admin2 last name")
        self.assertEqual(driver.license_number, "AAA11111")
        self.assertTrue(driver.check_password("3edczaq1"))


class DriverLicenseUpdateFormTests(TestCase):
    def test_valid_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12345"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "ABC12345")

    def test_invalid_length_license_number(self):
        form = DriverLicenseUpdateForm(data={"license_number": "AB123"})
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
        self.assertIn(
            "License number should consist of 8 characters",
            form.errors["license_number"]
        )

    def test_invalid_first_three_characters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abC12345"})
        self.assertFalse(form.is_valid())
        self.assertIn(
            "First 3 characters should be uppercase letters",
            form.errors["license_number"]
        )

    def test_invalid_last_five_characters(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC12ab5"})
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"]
        )


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="123456"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_search_by_name(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Tesla", country="USA")

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Tesla"
        )

        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Ford")


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="123456"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_search_by_username(self):
        Driver.objects.create_user(
            username="johndoe",
            password="password123",
            license_number="12345"
        )
        Driver.objects.create_user(
            username="janedoe",
            password="password123",
            license_number="67890"
        )
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=jane"
        )
        self.assertContains(response, "janedoe")
        self.assertNotContains(response, "johndoe")


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="123456"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_search_by_model(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        Car.objects.create(model="Focus", manufacturer=manufacturer)
        Car.objects.create(model="Mustang", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:car-list") + "?model=Focus")
        self.assertContains(response, "Focus")
        self.assertNotContains(response, "Mustang")
