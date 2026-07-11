from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str_return_correct_format(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Testcountry",
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}",
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username='TestUser',
            license_number='DGR327843',
            first_name='Testfirst',
            last_name='Userlast',
            password='123aszxjbyh31',
        )
        self.assertEqual(
            str(driver),
        f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="Testcountry",
        )
        car = Car.objects.create(model="testmodel", manufacturer=manufacturer)
        self.assertEqual(str(car), f"{car.model}")

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username="TestUser",
            license_number="DGR327843",
            password="1qazcded3",
        )
        self.assertEqual(driver.license_number, 'DGR327843')
        self.assertTrue(driver.check_password("1qazcded3"))

    def test_car_and_driver_many_to_many_relationship(self):
        manufacturer = Manufacturer.objects.create(name="Dacia", country="Romania")
        car = Car.objects.create(model="Logan power", manufacturer=manufacturer)
        driver1 = get_user_model().objects.create_user(
            username="TestUser1",
            license_number="DGR327833",
            password="ad12",
        )
        driver2 = get_user_model().objects.create_user(
            username="TestUser2",
            license_number="DGR327843",
            password="ad11",
        )
        car.drivers.add(driver1, driver2)
        self.assertEqual(car.drivers.count(), 2)
        self.assertIn(car, driver1.cars.all())
