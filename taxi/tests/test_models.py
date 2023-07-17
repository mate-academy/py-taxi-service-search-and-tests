from django.db.utils import IntegrityError
from django.test import TestCase

from taxi.models import Manufacturer, Driver
from django.contrib.auth import get_user_model


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_license_number_unique(self):
        license_number = "1234567890"
        username = "test_user"
        password = "test_password"

        Driver.objects.create_user(
            username=username, password=password, license_number=license_number
        )

        try:
            Driver.objects.create_user(
                username="another_user",
                password="another_password",
                license_number=license_number,
            )
        except IntegrityError:
            pass
        else:
            self.fail("An IntegrityError was expected")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="driver1",
            first_name="John",
            last_name="Connor",
            license_number="ABC123",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="driver1",
            first_name="John",
            last_name="Connor",
            license_number="ABC123",
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.pk}/")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        driver = get_user_model().objects.create_user(
            username="driver1",
            first_name="John",
            last_name="Connor",
            license_number="ABC123",
        )
        car = manufacturer.car_set.create(model="Camry")
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)
