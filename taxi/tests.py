from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number
from taxi.models import Car, Manufacturer

Driver = get_user_model()


class LicenseValidationTests(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_invalid_license_length(self):
        with self.assertRaises(ValidationError):
            validate_license_number("AB12345")
        with self.assertRaises(ValidationError):
            validate_license_number("ABCD12345")

    def test_invalid_license_prefix(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")
        with self.assertRaises(ValidationError):
            validate_license_number("12A12345")

    def test_invalid_license_suffix(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234a")
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234!")


class ToggleAssignToCarTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create_user(
            username="driver_one",
            password="StrongPassword123!",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_assign_and_remove_driver_from_car(self):
        url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.id})

        response = self.client.post(url)
        self.assertRedirects(
            response, reverse("taxi:car-detail", kwargs={"pk": self.car.id})
        )
        self.assertIn(self.driver, self.car.drivers.all())

        response = self.client.post(url)
        self.assertRedirects(
            response, reverse("taxi:car-detail", kwargs={"pk": self.car.id})
        )
        self.assertNotIn(self.driver, self.car.drivers.all())


class SearchFunctionalityTests(TestCase):
    def setUp(self):
        self.driver_alpha = Driver.objects.create_user(
            username="ivan_petrov",
            password="StrongPassword123!",
            license_number="AAA11111",
        )
        self.driver_beta = Driver.objects.create_user(
            username="petro_sidorov",
            password="StrongPassword123!",
            license_number="BBB22222",
        )
        self.manufacturer_a = Manufacturer.objects.create(
            name="Volkswagen", country="Germany"
        )
        self.manufacturer_b = Manufacturer.objects.create(
            name="Volvo", country="Sweden"
        )
        self.manufacturer_c = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car_a = Car.objects.create(
            model="Golf GTI", manufacturer=self.manufacturer_a
        )
        self.car_b = Car.objects.create(
            model="XC90", manufacturer=self.manufacturer_b
        )
        self.client.force_login(self.driver_alpha)

    def test_search_drivers_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "IVAN"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver_alpha.username)
        self.assertNotContains(response, self.driver_beta.username)

    def test_search_cars_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "golf"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car_a.model)
        self.assertNotContains(response, self.car_b.model)

    def test_search_manufacturers_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "vol"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer_a.name)
        self.assertContains(response, self.manufacturer_b.name)
        self.assertNotContains(response, self.manufacturer_c.name)

    def test_empty_search_returns_all_items(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer_a.name)
        self.assertContains(response, self.manufacturer_b.name)
        self.assertContains(response, self.manufacturer_c.name)
