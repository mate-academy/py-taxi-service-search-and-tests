from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="NI-SAN", country="Japan")
        self.assertEqual(manufacturer.name, "NI-SAN")
        self.assertEqual(manufacturer.country, "Japan")

    def test_driver_with_license(self):
        username = "admin"
        password = "admin12345"
        first_name = "Andrew"
        last_name = "Brown"
        license_number = "ASW12344"
        driver = Driver.objects.create_user(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            license_number=license_number)

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)

    def test_driver_str(self):
        username = "admin"
        password = "admin12345"
        first_name = "Andrew"
        last_name = "Brown"
        driver = Driver.objects.create_user(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name)

        self.assertEqual(str(driver), f"{username} ({first_name} {last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="NI-SAN", country="Japan")
        car = Car.objects.create(model="BMW", manufacturer=manufacturer)
        self.assertEqual(str(car), "BMW")
