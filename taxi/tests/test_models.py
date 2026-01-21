from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="RET",
            country="New Zeeland"
        )

        driver = Driver.objects.create(
            username="Bento",
            first_name="Benny",
            last_name="Hrozhyn",
        )

        car = Car.objects.create(
            model="Renault",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)
