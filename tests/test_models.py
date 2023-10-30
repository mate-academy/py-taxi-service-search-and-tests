from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str_method(self):
        """Test of custom str() function for Manufacturer"""
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    def test_driver_str_method(self):
        """Test of custom str() function for Driver"""
        driver = Driver.objects.create(
            username="test_user",
            first_name="test",
            last_name="test"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_licence_number_exist(self):
        """Test for existing Drivers licence_numer"""
        driver = Driver.objects.create(
            username="test_user",
            first_name="test",
            last_name="test",
            license_number="TEST12345"
        )
        self.assertEqual(driver.license_number, "TEST12345")

    def test_get_absolute_url_method(self):
        """Test of get_absolute_url() for Driver"""
        driver = Driver.objects.create(
            username="test_user",
            first_name="test",
            last_name="test",
            license_number="TEST12345"
        )
        url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), url)


class CarModelTest(TestCase):
    def test_car_str_method(self):
        """Test of custom str() function for Car"""
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        self.assertEqual(
            str(car), car.model
        )
