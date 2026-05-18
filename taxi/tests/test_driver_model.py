from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver


class DriverModelTests(TestCase):
    def test_driver_str_contains_username_and_full_name(self):
        driver = Driver.objects.create_user(
            username="john_driver",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="BBB12345",
        )

        self.assertEqual(str(driver), "john_driver (John Doe)")

    def test_driver_absolute_url(self):
        driver = Driver.objects.create_user(
            username="jane_driver",
            password="testpass123",
            license_number="CCC12345",
        )

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )
