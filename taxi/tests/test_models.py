from unittest import TestCase

from django.db.utils import IntegrityError

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test1",
                                                   country="test")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_create_unique_license_number(self):
        Driver.objects.create_user(
            username="test1",
            password="test1234",
            license_number="TST12345"
        )
        with self.assertRaises(IntegrityError):
            Driver.objects.create_user(
                username="test2",
                password="test1234",
                license_number="TST12345"
            )

    def test_driver_str(self):
        driver1 = Driver.objects.create_user(
            username="test2",
            password="test1234",
            first_name="test",
            last_name="test",
            license_number="TST12346"
        )
        self.assertEqual(
            str(driver1),
            f"{driver1.username} ({driver1.first_name} {driver1.last_name})"
        )

    def test_car_str(self):
        temp_manufacturer = Manufacturer.objects.create(name="test",
                                                        country="test")
        car = Car.objects.create(model="test", manufacturer=temp_manufacturer)

        self.assertEqual(str(car), car.model)
