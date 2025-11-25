from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer(name="Toyota", country="Japan")
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_driver_str(self):
        driver = Driver(username="johndoe", first_name="John", last_name="Doe")
        self.assertEqual(str(driver), "johndoe (John Doe)")

    def test_car_str(self):
        car = Car(model="Corolla")
        self.assertEqual(str(car), "Corolla")

    def test_create_driver_with_license_number(self):
        driver = Driver.objects.create_user(
            username="janedoe",
            license_number="ABC123"
        )
        self.assertEqual(driver.license_number, "ABC123")
