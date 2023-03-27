from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car, Driver


class ModelTest(TestCase):
    def test_manufacturer_format_str(self):
        format_ = Manufacturer.objects.create(
            name="Test123",
            country="CountryTest"
        )
        self.assertEqual(
            str(format_),
            f"{format_.name} {format_.country}"
        )

    def test_car_format_str(self):
        format_ = Car.objects.create(
            model="S6",
            manufacturer=Manufacturer.objects.create(
                name="Audi",
                country="Germany"
            ),
        )
        self.assertEqual(str(format_), format_.model)

    def test_driver_format_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            first_name="test_name",
            last_name="test_last_name",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_license_create(self):
        username = "test"
        license_number = "ABA12345"
        password = "testPass1234"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name="test_name",
            last_name="test_last_name",
            license_number=license_number
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test_user",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            "/drivers/1/"
        )

    def test_driver_verbose_name(self):
        self.assertEqual(Driver._meta.verbose_name, "driver")

    def test_driver_verbose_name_plural(self):
        self.assertEqual(Driver._meta.verbose_name_plural, "drivers")

    def test_manufacturers_ordering(self):
        self.assertEqual(Manufacturer._meta.ordering, ["name"])
