from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        format_ = Manufacturer.objects.create(name="BMW", country="Germany")
        self.assertEquals(str(format_), f"{format_.name} {format_.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="admin",
            password="admin123",
            first_name="admin first",
            last_name="admin last"
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_create_driver_with_license_number(self):
        username = "test_username"
        password = "test_password"
        license_number = "FVF45678"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)

    def test_car_str(self):
        name = "test_name"
        country = "test_country"
        model = "test_model"
        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )
        self.assertEquals(str(car), car.model)
