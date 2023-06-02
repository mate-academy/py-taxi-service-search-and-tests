from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Test name",
            country="Test country"
        )
        driver = Driver.objects.create(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last"
        )
        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer
        )
        car.drivers.set([driver])

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"

        self.assertEqual(str(manufacturer), expected_object_name)

    def test_manufacturer_meta_ordering(self):
        expected_ordering = ["name"]
        manufacturer_ordering = Manufacturer._meta.ordering
        self.assertListEqual(manufacturer_ordering, expected_ordering)

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        expected_object_name = f"{driver.username} " \
                               f"({driver.first_name} {driver.last_name})"
        self.assertEqual(str(driver), expected_object_name)

    def test_driver_get_absolute_url(self):
        author = Driver.objects.get(id=1)
        self.assertEqual(
            author.get_absolute_url(),
            "/drivers/1/"
        )

    def test_car_str(self):
        car = Car.objects.get(id=1)
        expected_object_name = f"{car.model}"
        self.assertEqual(str(car), expected_object_name)
