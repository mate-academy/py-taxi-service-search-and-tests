from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    def test_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name",
                                                   country="test_country")
        self.assertEquals(f"{manufacturer.name} {manufacturer.country}",
                          str(manufacturer))


class DriverModelTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create(first_name="Driver",
                                            last_name="Test")

    def test_get_absolute_url(self):
        expected_url = reverse("taxi:driver-detail",
                               kwargs={"pk": self.driver.pk})
        actual_url = self.driver.get_absolute_url()
        self.assertEqual(actual_url, expected_url)

    def test_str(self):
        self.assertEqual(str(self.driver),
                         f"{self.driver.username} "
                         f"({self.driver.first_name} "
                         f"{self.driver.last_name})")

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "12345"
        license_number = "ADF12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))


class CarModelTest(TestCase):

    def test_str(self):
        manufacturer = Manufacturer.objects.create(name="test_name",
                                                   country="test_country")
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        self.assertEqual(car.model, str(car))
