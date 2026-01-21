from django.test import TestCase
from taxi.models import (Manufacturer,
                         Driver,
                         Car)


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="TestName",
                                                   country="TestCountry")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create(username="TestUserName",
                                       first_name="TestFirstName",
                                       last_name="TestLastName"
                                       )
        self.assertEqual(str(driver),
                         f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="TestName",
                                                   country="TestCountry")
        car = Car.objects.create(model="TestModel",
                                 manufacturer=manufacturer,
                                 )
        self.assertEqual(str(car),
                         car.model)

    def test_get_driver_absolute_url(self):
        driver = Driver.objects.create(username="TestUserName",
                                       first_name="TestFirstName",
                                       last_name="TestLastName"
                                       )
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
