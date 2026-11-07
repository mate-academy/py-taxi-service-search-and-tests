from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="VAG",
                                                   country="Germany"
                                                   )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="Zebra", country="USA")
        Manufacturer.objects.create(name="Alpha", country="UK")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            [manufacturer.name for manufacturer in manufacturers],
            ["Alpha", "Zebra"]
        )

    def test_driver_verbose_name(self):
        meta = Driver._meta

        self.assertEqual(meta.verbose_name, "driver")

        self.assertEqual(meta.verbose_name_plural, "drivers")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolut_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="VAG",
                                                   country="Germany"
                                                   )
        car = Car.objects.create(model="Skoda", manufacturer=manufacturer)
        self.assertEqual(
            str(car),
            car.model
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test123"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(
            driver.username,
            username
        )
        self.assertEqual(
            driver.license_number,
            license_number
        )
        self.assertTrue(
            driver.check_password(password)
        )
