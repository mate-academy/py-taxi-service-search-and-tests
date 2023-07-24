from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        name = "Koeninsegg"
        country = "Sweden"
        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )
        self.assertEqual(str(manufacturer), f"{name} {country}")

    def test_driver_str(self):
        username = "Bobber"
        first_name = "Bob"
        last_name = "Obber"
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
        username = "Bobber"
        password = "IamStrongPassword11"
        first_name = "Bob"
        last_name = "Obber"
        license_number = "ABC12345"
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

    def test_car_str(self):
        model = "Celica"
        manufacturer = Manufacturer.objects.create(
            name="Toyota"
        )
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), model)
