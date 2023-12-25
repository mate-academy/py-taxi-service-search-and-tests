from django.test import TestCase

from taxi.models import Driver, Manufacturer


class ModelTests(TestCase):
    def test_driver(self):
        driver = Driver.objects.create_user(username="test",
                                            password="<PASSWORD>",
                                            license_number="12345")
        self.assertTrue(driver.check_password("<PASSWORD>"))
        self.assertEqual(driver.license_number, "12345")

    def test_manufacturer(self):
        manufacturer = Manufacturer.objects.create(name="BMW",
                                                   country="Germany")
        self.assertEqual(manufacturer, Manufacturer.objects.get(id=1))
