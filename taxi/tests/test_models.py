from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="bob",
            first_name="bob",
            last_name="king"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        Driver.objects.create(username="Big", last_name="Bob")
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Volkswagen",
            country="Germany"
        )
        car = Car.objects.create(model="Golf", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
