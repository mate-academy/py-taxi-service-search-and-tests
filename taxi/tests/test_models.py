from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Driver.objects.create_user(
            username="testdriver",
            first_name="test_first",
            last_name="test_last",
            password="test123",
            license_number="test_number"
        )

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        expected_object_name = (
            f"{driver.username} "
            f"({driver.first_name} {driver.last_name})"
        )
        self.assertEqual(str(driver), expected_object_name)

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_driver_with_licence_number(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.username, "testdriver")
        self.assertEqual(driver.license_number, "test_number")
        self.assertTrue(driver.check_password("test123"))


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_object_name)


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )

    def test_car_str(self):
        car = Car.objects.first()
        self.assertEqual(str(car), car.model)
