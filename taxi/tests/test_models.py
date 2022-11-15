from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class ModelsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            first_name='George',
            last_name='Michael',
            license_number="ABC12345"
        )

        Manufacturer.objects.create(
            name="Ford Motor Company", country="USA")

    def test_driver_model_str(self):
        driver = Driver.objects.create(
            username="george.michael",
            first_name="George", last_name="Michael")
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), '/drivers/1/')

    def test_manufacturer_model_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_car_model_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)
