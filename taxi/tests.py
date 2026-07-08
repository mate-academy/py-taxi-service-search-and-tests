from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Car, Driver, Manufacturer


class DriverModelTests(TestCase):
    def test_driver_str_returns_username_and_full_name(self):
        driver = Driver.objects.create_user(
            username="driver",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )

        self.assertEqual(str(driver), "driver (John Doe)")


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str_returns_name_and_country(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.assertEqual(str(manufacturer), "Toyota Japan")


class CarModelTests(TestCase):
    def test_car_str_returns_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        car = Car.objects.create(model="Corolla", manufacturer=manufacturer)

        self.assertEqual(str(car), "Corolla")


class DriverLicenseFormTests(TestCase):
    def test_creation_form_accepts_valid_license_number(self):
        form = DriverCreationForm(
            data={
                "username": "driver",
                "password1": "strong-pass123",
                "password2": "strong-pass123",
                "license_number": "ABC12345",
                "first_name": "John",
                "last_name": "Doe",
            }
        )

        self.assertTrue(form.is_valid())

    def test_update_form_rejects_license_number_with_wrong_length(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABC1234"})

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_update_form_rejects_license_number_without_uppercase_prefix(self):
        form = DriverLicenseUpdateForm(data={"license_number": "abc12345"})

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_update_form_rejects_license_number_without_numeric_suffix(self):
        form = DriverLicenseUpdateForm(data={"license_number": "ABCDE123"})

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class LoginRequiredViewTests(TestCase):
    def test_driver_list_requires_login(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)
        self.assertIn("/accounts/login/", response.url)


class SearchViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test12345",
            license_number="TST12345",
        )
        cls.driver = Driver.objects.create_user(
            username="alex_driver",
            password="test12345",
            license_number="ALX12345",
        )
        cls.other_driver = Driver.objects.create_user(
            username="bob_driver",
            password="test12345",
            license_number="BOB12345",
        )
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        cls.car = Car.objects.create(model="Corolla", manufacturer=toyota)
        cls.other_car = Car.objects.create(model="X5", manufacturer=bmw)

    def setUp(self):
        self.client.force_login(self.user)

    def test_driver_search_filters_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "alex"},
        )

        self.assertContains(response, self.driver.username)
        self.assertNotContains(response, self.other_driver.username)

    def test_car_search_filters_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "coro"},
        )

        self.assertContains(response, self.car.model)
        self.assertNotContains(response, self.other_car.model)

    def test_manufacturer_search_filters_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": "toy"},
        )

        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_search_query_is_available_in_context(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "alex"},
        )

        self.assertEqual(response.context["query"], "alex")
