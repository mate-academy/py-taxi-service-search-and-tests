from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Manufacturer.objects.create(
            name="Audi",
            country="Germany",
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturer_ordering(self):
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(manufacturers),
            sorted(manufacturers, key=lambda manufacturer: manufacturer.name)
        )


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            username="test_driver",
            password="password",
            license_number="TLN001"
        )

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_verbose_names(self):
        driver = Driver.objects.get(id=1)
        verbose_name = driver._meta.verbose_name
        verbose_name_plural = driver._meta.verbose_name_plural
        self.assertEqual(verbose_name, "driver")
        self.assertEqual(verbose_name_plural, "drivers")

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        driver = Driver.objects.create(
            username="test_driver",
            password="password",
            license_number="TLN001"
        )
        Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        car = Car.objects.create(
            model="Corolla",
            manufacturer=Manufacturer.objects.get(id=1),
        )
        car.drivers.add(driver)

    def test_car_str(self):
        car = Car.objects.get(id=1)
        self.assertEqual(str(car), f"{car.model}")
