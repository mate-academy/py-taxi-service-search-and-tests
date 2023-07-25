from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_car_str(self):
        model = "Camry"
        manufacturer = Manufacturer.objects.create(
            name="Toyota"
        )
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), model)

    def test_manufacturer_str(self):
        name = "BMW"
        country = "Germany"
        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )
        self.assertEqual(str(manufacturer), f"{name} {country}")

    def test_driver_str(self):
        username = "johndoe"
        first_name = "John"
        last_name = "Doe"
        driver = Driver.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        self.assertEqual(
            str(driver),
            f"{username} ({first_name} {last_name})"
        )

    def test_create_driver_with_license(self):
        username = "johndoe"
        password = "Very$trongPassw0rd"
        first_name = "John"
        last_name = "Doe"
        license_number = "JPN13248"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))
