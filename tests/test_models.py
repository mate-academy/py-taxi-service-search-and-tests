from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        name = "TestManufacturer"
        country = "TestCountry"
        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country,
        )

        self.assertEquals(str(manufacturer), f"{name} {country}")

    def test_driver_str(self):
        username = "TestUsername"
        first_name = "TestFirstName"
        last_name = "TestLast"
        driver = Driver.objects.create_user(
            username=username,
            password="test1234",
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEquals(
            str(driver), f"{username} ({first_name} {last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry",
        )
        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer
        )

        self.assertEquals(str(car), "TestModel")

    def test_create_driver_with_license(self):
        username = "TestUsername"
        password = "test1234"
        license_number = "TestLicense"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEquals(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)
