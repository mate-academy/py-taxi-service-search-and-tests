from django.test import TestCase
from taxi.models import Driver, Manufacturer, Car


class DriverModelTest(TestCase):
    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="driver1", password="pass12345",
            first_name="John", last_name="Doe",
            license_number="ABC12345"
        )
        self.assertEqual(str(driver), "driver1 (John Doe)")
