from django.test import TestCase
from taxi.models import Driver


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(
            username="test_driver",
            password="password"
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.username, "test_driver")
