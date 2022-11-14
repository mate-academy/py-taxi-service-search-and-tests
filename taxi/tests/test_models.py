from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class CarModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        driver = Driver.objects.create(
            username="user_name",
            password="user12345"
        )
        car = Car.objects.create(
            model="Toyota Yaris",
            manufacturer=manufacturer
        )
        car.drivers.add(driver)

    def test_car_str(self):
        car = Car.objects.get(id=1)

        self.assertEqual(str(car), f"{car.model}")


class DriverModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="user_name",
            password="user12345",
            license_number="ABC78965",
            first_name="user",
            last_name="name"
        )

    def test_create_driver_with_license_number(self):
        driver = Driver.objects.get(id=1)
        field_label = driver._meta.get_field("license_number").verbose_name

        self.assertEqual(driver.username, "user_name")
        self.assertTrue(driver.check_password("user12345"))
        self.assertEqual(field_label, "license number")

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
