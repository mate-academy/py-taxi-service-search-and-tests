from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestModels(TestCase):
    def test_manufacturer_str(self) -> None:
        manu = Manufacturer.objects.create(name="Citroen",
                                           country="France")
        self.assertEqual(str(manu), f"{manu.name} {manu.country}")

    def test_driver_str(self) -> None:
        driver = Driver.objects.create(username="testi",
                                       password="pastest",
                                       first_name="Test",
                                       last_name="Testovich")
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        manu = Manufacturer.objects.create(name="Citroen",
                                           country="France")
        car = Car.objects.create(model="C4", manufacturer=manu)

        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license(self) -> None:
        username = "Testill"
        password = "pastest"
        license_num = "ATB98765"
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_num
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.license_number, license_num)
