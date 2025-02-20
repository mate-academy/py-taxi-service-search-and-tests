from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    CarModelSearchForm,
    ManufacturerNameSearchForm,
    DriverUsernameSearchForm,
)
from taxi.models import Manufacturer, Driver, Car


class CarModelSearchFormTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(name="Toyota")
        driver = get_user_model().objects.create_user(
            username="ihorlister",
            password="fads4fadsf*wing",
            first_name="Ihor",
            last_name="Lister",
            license_number="RVW3461",
        )

        Car.objects.create(model="Camry", manufacturer=manufacturer)
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="Sedan", manufacturer=manufacturer)

        car_with_driver = Car.objects.create(
            model="Highlander", manufacturer=manufacturer
        )
        car_with_driver.drivers.add(driver)

        self.client.force_login(driver)

    def test_valid_form(self):
        form = CarModelSearchForm(data={"model": "Sedan"})
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = CarModelSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CarModelSearchForm(data={"model": "A" * 300})
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)

    def test_view_with_search(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Camry"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Camry")
        self.assertNotContains(response, "Corolla")
        self.assertNotContains(response, "Sedan")

    def test_view_without_search(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertContains(response, "Corolla")
        self.assertContains(response, "Sedan")


class ManufacturerNameSearchFormTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")

        driver = get_user_model().objects.create_user(
            username="ihorlister",
            password="fads4fadsf*wing",
            first_name="Ihor",
            last_name="Lister",
            license_number="RVW3461",
        )

        self.client.force_login(driver)

    def test_valid_form(self):
        form = ManufacturerNameSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = ManufacturerNameSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ManufacturerNameSearchForm(data={"name": "A" * 300})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_view_with_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
        self.assertNotContains(response, "BMW")

    def test_view_without_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": ""}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")
        self.assertContains(response, "BMW")


class DriverUsernameSearchFormTest(TestCase):
    def setUp(self):
        Driver.objects.create(
            username="john_doe",
            password="password123",
            license_number="RVW4527"
        )
        Driver.objects.create(
            username="jane_smith",
            password="password456",
            license_number="RVW3426"
        )
        Driver.objects.create(
            username="jack_black",
            password="password789",
            license_number="RTY7316"
        )
        driver = get_user_model().objects.create_user(
            username="ihorlister",
            password="fads4fadsf*wing",
            first_name="Ihor",
            last_name="Lister",
            license_number="RVW3461",
        )
        self.client.force_login(driver)

    def test_valid_form(self):
        form = DriverUsernameSearchForm(data={"username": "john_doe"})
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = DriverUsernameSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = DriverUsernameSearchForm(data={"username": "A" * 300})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_view_with_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "john"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")
        self.assertNotContains(response, "jack_black")

    def test_view_without_search(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "john_doe")
        self.assertContains(response, "jane_smith")
        self.assertContains(response, "jack_black")
