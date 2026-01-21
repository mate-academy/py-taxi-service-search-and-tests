from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="test",
            password="test12345",
            first_name="Bob",
            last_name="Bobsky",
        )

    def test_driver_str_method(self):
        driver = Driver.objects.get(id=1)
        expected_object_name = (
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertEquals(expected_object_name, str(driver))

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEquals(driver.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="OOO", country="Germany"
        )
        Car.objects.create(model="X5", manufacturer_id=manufacturer.id)

    def test_car_str_method(self):
        expected_object_name = "X5"
        self.assertEquals(expected_object_name, str(Car.objects.get(id=1)))


class ManufacturerModelTest(TestCase):
    def test_car_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test_country"
        )
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEquals(expected_object_name, str(manufacturer))
