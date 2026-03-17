from django.test import TestCase
from taxi.models import Driver


class DriverModelTest(TestCase):
    def test_driver_model(self):
        driver = Driver.objects.create(
            username="admin",
            first_name="Marco",
            last_name="Williams",
            license_number="123456",
        )
        self.assertEqual(str(driver), "admin (Marco Williams)")
        self.assertEqual(driver.license_number, "123456")
