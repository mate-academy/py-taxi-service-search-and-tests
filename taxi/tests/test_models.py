from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="test",
            country="test_country",
        )

    def test_create_manufacturer(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(manufacturer.name, "test")
        self.assertEqual(manufacturer.country, "test_country")

    def test_str_representation(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )

    def test_car_creation_with_fk_and_m2m(self):
        Driver.objects.create_user(
            username="test1", password="test123", license_number="TST12345"
        )
        Driver.objects.create_user(
            username="test2", password="test123", license_number="TST54321"
        )
        drivers = Driver.objects.all()
        car = Car.objects.get(id=1)
        car.drivers.set(drivers)
        self.assertEqual(car.manufacturer.name, "test_manufacturer")
        self.assertEqual(car.drivers.count(), 2)
        self.assertEqual(list(car.drivers.all()), list(drivers))

    def test_str_representation(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), car.model)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="test",
            password="test123",
            license_number="TST12345",
        )

    def test_driver_creation_with_licence_number(self):
        username = "test_driver"
        password = "test123"
        license_number = "TST54321"
        driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_str_representation(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")
