from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test.user",
            password="password123",
            first_name="First",
            last_name="Last",
            license_number="ABC12345"
        )
        self.assertEqual(str(driver), "test.user (First Last)")

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test.user",
            license_number="ABC12345"
        )
        url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), url)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        car = Car.objects.create(model="Model S", manufacturer=manufacturer)
        self.assertEqual(str(car), "Model S")


class FormTests(TestCase):
    def test_driver_license_number_validation(self):
        from taxi.forms import validate_license_number
        from django.core.exceptions import ValidationError

        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")

        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234A")


class PrivateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="password123",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="TestMake", country="TestCountry"
        )
        self.car = Car.objects.create(
            model="TestModel", manufacturer=self.manufacturer
        )

    def test_retrieve_manufacturers_with_search(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Honda", country="Japan")

        res = self.client.get(reverse(
            "taxi:manufacturer-list"),
            {"name": "Toyota"}
        )
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "Honda")

    def test_retrieve_cars_with_search(self):
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        Car.objects.create(model="Civic", manufacturer=self.manufacturer)

        res = self.client.get(reverse("taxi:car-list"), {"model": "Camry"})
        self.assertContains(res, "Camry")
        self.assertNotContains(res, "Civic")

    def test_retrieve_drivers_with_search(self):
        get_user_model().objects.create_user(
            username="driver.one", license_number="AAA11111"
        )
        get_user_model().objects.create_user(
            username="driver.two", license_number="BBB22222"
        )

        res = self.client.get(reverse(
            "taxi:driver-list"),
            {"username": "driver.one"}
        )
        self.assertContains(res, "driver.one")
        self.assertNotContains(res, "driver.two")
