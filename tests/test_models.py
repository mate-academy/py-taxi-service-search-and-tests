from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def test_models_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        driver = Driver.objects.create(
            username="Test Driver",
            first_name="Test Driver First",
            last_name="Test Driver Last",
        )
        car = Car.objects.create(
            model="Test Car",
            manufacturer=manufacturer
        )
        self.assertEqual(str(manufacturer), "Test Manufacturer Test Country")
        self.assertEqual(
            str(driver),
            "Test Driver (Test Driver First Test Driver Last)"
        )
        self.assertEqual(str(car), "Test Car")

    def test_create_models(self):
        manufacturer_name = "Test Manufacturer"
        manufacturer_country = "Test Country"
        driver_username = "Test Driver"
        driver_first_name = "Test Driver First"
        driver_last_name = "Test Driver Last"
        car_model = "Test Car"

        manufacturer = Manufacturer.objects.create(
            name=manufacturer_name,
            country=manufacturer_country,
        )
        driver = Driver.objects.create(
            username=driver_username,
            first_name=driver_first_name,
            last_name=driver_last_name,
        )
        car = Car.objects.create(
            model=car_model,
            manufacturer=manufacturer
        )
        self.assertEqual(manufacturer.name, manufacturer_name)
        self.assertEqual(manufacturer.country, manufacturer_country)
        self.assertEqual(driver.username, driver_username)
        self.assertEqual(driver.first_name, driver_first_name)
        self.assertEqual(driver.last_name, driver_last_name)
        self.assertEqual(car.model, car_model)
        self.assertEqual(car.manufacturer.name, manufacturer_name)
