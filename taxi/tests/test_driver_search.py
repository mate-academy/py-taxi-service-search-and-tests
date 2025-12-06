from django.test import TestCase
from taxi.models import Driver


class DriverSearchTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.driver1 = Driver.objects.create(
            username="test_driver1",
            email="driver1@example.com",
            license_number="ABC123"
        )
        cls.driver2 = Driver.objects.create(
            username="test_driver2",
            email="driver2@example.com",
            license_number="XYZ789"
        )
        cls.driver3 = Driver.objects.create(
            username="alpha_driver",
            email="alpha@example.com",
            license_number="DEF456"
        )

    def test_search_driver_by_username_existing(self):
        results = Driver.objects.filter(username__icontains="test_driver")
        self.assertEqual(len(results), 2)
        self.assertIn(self.driver1, results)
        self.assertIn(self.driver2, results)

    def test_search_driver_by_username_non_existing(self):
        results = Driver.objects.filter(username__icontains="non_existent")
        self.assertEqual(len(results), 0)

    def test_partial_search_driver(self):
        results = Driver.objects.filter(username__icontains="alpha")
        self.assertEqual(len(results), 1)
        self.assertIn(self.driver3, results)
