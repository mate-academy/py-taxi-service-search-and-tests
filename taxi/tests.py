from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from taxi.forms import validate_license_number
from taxi.models import Car, Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_driver_str_and_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="driver",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )

        self.assertEqual(str(driver), "driver (John Doe)")
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        car = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), "Corolla")


class LicenseValidationTests(TestCase):
    def test_valid_license_number(self):
        self.assertEqual(validate_license_number("ABC12345"), "ABC12345")

    def test_license_number_must_have_eight_characters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABC1234")

    def test_license_number_must_start_with_uppercase_letters(self):
        with self.assertRaises(ValidationError):
            validate_license_number("abc12345")

    def test_license_number_must_end_with_digits(self):
        with self.assertRaises(ValidationError):
            validate_license_number("ABCDE123")


class PublicViewTests(TestCase):
    def test_login_required_for_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="john",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)

    def test_index_displays_amounts(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)

    def test_toggle_assign_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        car = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer,
        )

        self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": car.pk})
        )

        self.assertIn(car, self.driver.cars.all())


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="test12345",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)

    def test_driver_search_by_username(self):
        john = get_user_model().objects.create_user(
            username="john_driver",
            password="test12345",
            license_number="BBB22222",
        )
        get_user_model().objects.create_user(
            username="mary_driver",
            password="test12345",
            license_number="CCC33333",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"query": "john"},
        )

        self.assertEqual(list(response.context["driver_list"]), [john])

    def test_car_search_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        corolla = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Camry",
            manufacturer=manufacturer,
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"query": "roll"},
        )

        self.assertEqual(list(response.context["car_list"]), [corolla])

    def test_manufacturer_search_by_name(self):
        toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Manufacturer.objects.create(
            name="Honda",
            country="Japan",
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"query": "yot"},
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [toyota],
        )
