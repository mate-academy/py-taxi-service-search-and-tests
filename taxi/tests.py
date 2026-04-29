from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car
from taxi.forms import DriverLicenseUpdateForm


class FormTest(TestCase):
    def test_license_number_validation(self):
        form_data = {"license_number": "ABC12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {"license_number": "ABCD2345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Last 5 characters should be digits",
            form.errors["license_number"],
        )


class SearchTest(TestCase):
    def test_driver_search_by_username(self):
        Driver.objects.create_user(
            username="test1",
            password="racer2242",
            license_number="ABC12345",
        )
        Driver.objects.create_user(
            username="test2",
            password="racer4424",
            license_number="CBA12345",
        )
        self.client.login(
            username="test1",
            password="racer2242"
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "unique"})
        self.assertContains(response, "test1")
        self.assertNotContains(response, "test2")

    def test_manufacturer_search_by_name(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )

        self.client.force_login(user)

        Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(
            url,
            {"name": "Tes"}
        )
        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Toyota")

        response = self.client.get(url, {"name": ""})

        self.assertContains(response, "Tesla")
        self.assertContains(response, "Toyota")

    def test_car_search_by_model(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        Car.objects.create(
            model="Model S",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Model X",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="Civic",
            manufacturer=manufacturer
        )
        self.client.force_login(user)

        url = reverse("taxi:car-list")

        response = self.client.get(url, {"model": "Model"})
        self.assertContains(response, "Model S")
        self.assertContains(response, "Model X")
        self.assertNotContains(response, "Civic")
        response = self.client.get(url, {"model": ""})
        self.assertContains(response, "Civic")


class AccessTest(TestCase):
    def test_car_list_login_required(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertIn("/accounts/login/", response.url)
