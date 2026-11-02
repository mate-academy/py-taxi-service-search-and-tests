from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer(name="Audi", country="Germany")
        self.assertEqual(str(manufacturer), "Audi Germany")

    def test_car_str(self):
        car = Car(model="A4")
        self.assertEqual(str(car), "A4")

    def test_driver_str(self):
        driver = get_user_model()(
            username="test", first_name="Test", last_name="Driver"
        )
        self.assertEqual(str(driver), "test (Test Driver)")

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test", license_number="TST12345"
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="TST12345",
        )
        self.assertEqual(driver.username, "test")
        self.assertEqual(driver.license_number, "TST12345")
        self.assertTrue(driver.check_password("test12345"))
