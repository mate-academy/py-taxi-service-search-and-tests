from django.test import TestCase
from taxi.models import Driver, Car, Manufacturer


class CarModelTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), car.model)

    def test_car_manufacturer_relation(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.assertEqual(car.manufacturer.name, "Toyota")

    def test_car_drivers_relation(self):
        driver = Driver.objects.create(
            username="John",
            license_number="ABC12345"
        )
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car = Car.objects.create(model="X5", manufacturer=manufacturer)
        car.drivers.add(driver)
        self.assertIn(driver, car.drivers.all())

    def test_car_manufacturer_cascade_delete(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        car = Car.objects.create(model="A4", manufacturer=manufacturer)
        manufacturer.delete()
        self.assertFalse(Car.objects.filter(id=car.id).exists())


class DriverModelTest(TestCase):
    def test_driver_str(self):
        username = "testuser"
        first_name = "Test"
        last_name = "Test"
        driver = Driver.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            license_number="ABC12345",
        )
        self.assertEqual(str(driver), f"{username} ({first_name} {last_name})")

    def test_license_number_unique(self):
        Driver.objects.create(
            username="driver1",
            license_number="ABC12345"
        )
        with self.assertRaises(Exception):
            Driver.objects.create(
                username="driver2",
                license_number="ABC12345"
            )

    def test_driver_absolute_url(self):
        driver = Driver.objects.create(
            username="john",
            license_number="ABC12345"
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.pk}/")


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        name = "Ford"
        country = "Germany"
        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )
        self.assertEqual(str(manufacturer), f"{name} {country}")

    def test_name_unique(self):
        Manufacturer.objects.create(name="driver1", country="test_country1")
        with self.assertRaises(Exception):
            Manufacturer.objects.create(
                name="driver1",
                country="test_country2")
