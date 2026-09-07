from django.test import TestCase


from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):

    def test_manufacturer_format_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_format_str(self):
        driver = Driver.objects.create(
            username="test_username",
            first_name="test_first",
            last_name="test_last",
            license_number="GGG55555"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_format_str(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(
                name="test_name",
                country="test_country"
            )
        )
        self.assertEqual(str(car), "test_model")

    def test_driver_license_number(self):
        driver = Driver.objects.create(
            username="test_username",
            first_name="test_first",
            last_name="test_last",
            license_number="GGG55555"
        )
        assert driver.license_number == "GGG55555"
