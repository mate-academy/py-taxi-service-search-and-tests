from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        format_ = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )

        self.assertEqual(str(format_), f"{format_.name} {format_.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first",
            last_name="test_last"
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_model", country="test_country"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license(self):
        username = "test_username"
        password = "password2145"
        license_number = "test_license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.assertEqual(str(driver.username), username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(str(driver.license_number), license_number)
