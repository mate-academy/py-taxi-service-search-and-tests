from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        get_user_model().objects.create_user(
            username="Test username",
            password="test1234",
            first_name="Test firstname",
            last_name="Test lastname",
            license_number="Test license",
        )

        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test country",
        )

        Car.objects.create(model="Test model",
                           manufacturer=manufacturer)

    def test_manufacturer_str(self):
        # Getting an object for testing
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str_and_password(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertTrue(driver.check_password("test1234"))

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)

        # This will also fail if the urlconf is not defined.
        self.assertEquals(driver.get_absolute_url(), "/drivers/1/")

    def test_first_name_label(self):
        driver = Driver.objects.get(id=1)
        field_label = driver._meta.get_field("first_name").verbose_name
        self.assertEquals(field_label, "first name")

    def test_create_driver_license_number(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver.license_number, "Test license")

    def test_car_str(self):
        car = Car.objects.get(id=1, manufacturer_id=1)

        self.assertEqual(str(car), car.model)
