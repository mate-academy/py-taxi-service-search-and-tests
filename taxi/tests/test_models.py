from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        name = "test"
        country = "test country"
        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )
        self.assertEquals(str(manufacturer), f"{name} {country}")

    def test_create_driver_with_license_number(self):
        username = "test.username"
        password = "test_password"
        license_number = "TST12345"
        driver = get_user_model().objects.create_user(
            license_number=license_number,
            username=username,
            password=password,
        )
        self.assertEquals(driver.license_number, license_number)
        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))

    def test_driver_str(self):
        username = "test.username"
        password = "test_password"
        license_number = "TST12345"
        first_name = "test_first"
        last_name = "test_last"
        driver = get_user_model().objects.create_user(
            license_number=license_number,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        self.assertEquals(
            str(driver),
            f"{username} ({first_name} {last_name})"
        )

    def test_driver_absolute_url(self):
        id_ = 25
        username = "test.username"
        password = "test_password"
        license_number = "TST12345"
        driver = get_user_model().objects.create_user(
            id=id_,
            license_number=license_number,
            username=username,
            password=password,
        )
        self.assertEquals(driver.get_absolute_url(), f"/drivers/{id_}/")

    def test_car_str(self):
        model = "Test Model"
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test country"
        )
        car = Car(
            model=model,
            manufacturer=manufacturer
        )
        self.assertEquals(str(car), model)
