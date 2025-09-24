from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import ValidationError
from taxi.models import Manufacturer, Car, Driver
from taxi.forms import (
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm,
    validate_license_number,
)


class ModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="test12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "driver1 (John Doe)")

    def test_car_str(self):
        self.assertEqual(str(self.car), "Corolla")


class FormTest(TestCase):
    def test_valid_license_number(self):
        valid_license = "ABC12345"
        self.assertEqual(validate_license_number(valid_license), valid_license)

    def test_invalid_license_number_length(self):
        with self.assertRaisesMessage(
                ValidationError,
                "License number should consist of 8 characters"
        ):
            validate_license_number("AB12")

    def test_invalid_license_number_format_letters(self):
        with self.assertRaisesMessage(
                ValidationError,
                "First 3 characters should be uppercase letters"
        ):
            validate_license_number("abC12345")

    def test_invalid_license_number_format_digits(self):
        with self.assertRaisesMessage(
                ValidationError,
                "Last 5 characters should be digits"
        ):
            validate_license_number("ABC12abC")

    def test_car_search_form_valid(self):
        form = CarSearchForm(data={"model": "Corolla"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_valid(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_valid(self):
        form = DriverSearchForm(data={"username": "driver1"})
        self.assertTrue(form.is_valid())


class ViewTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford", country="USA"
        )
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="test12345",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="test12345",
            license_number="DEF67890"
        )
        self.client.login(username="driver1", password="test12345")
        self.car1 = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Focus", manufacturer=self.manufacturer2
        )

    def test_manufacturer_search_view(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Toyota"})
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_car_search_view(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Corolla"})
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

    def test_driver_search_view(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "driver1"})
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    # Tests for empty/missing queries returning full list
    def test_manufacturer_list_empty_query_returns_all(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": ""})
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")

    def test_manufacturer_list_no_query_returns_all(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")

    def test_car_list_empty_query_returns_all(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": ""})
        self.assertContains(response, "Corolla")
        self.assertContains(response, "Focus")

    def test_car_list_no_query_returns_all(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertContains(response, "Corolla")
        self.assertContains(response, "Focus")

    def test_driver_list_empty_query_returns_all(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": ""})
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")

    def test_driver_list_no_query_returns_all(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")

    # Tests for non-matching queries returning no results
    def test_manufacturer_search_no_results(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "NonExistentManufacturer"})
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_car_search_no_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "NonExistentCar"})
        self.assertNotContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

    def test_manufacturer_list_template_and_context(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], ManufacturerSearchForm)

    def test_car_list_template_and_context(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)

    def test_driver_list_template_and_context(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], DriverSearchForm)
