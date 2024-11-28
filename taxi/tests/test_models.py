from django.test import TestCase

from taxi.models import Manufacturer, Driver


class ModelsTest(TestCase):
    def test_create_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="Toyota",
                                                   country="Japan")
        self.assertEqual(manufacturer.name, "Toyota")

    def test_create_license(self):
        username = "test"
        password = "test"
        license_number = "QWE12345"
        driver = Driver.objects.create_user(username=username,
                                            password=password,
                                            license_number=license_number)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
