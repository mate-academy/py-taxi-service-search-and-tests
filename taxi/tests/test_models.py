from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_ordering(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(manufacturers[0].name, "Audi")


class DriverModelTest(TestCase):
    def test_str_method(self):
        driver = Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(str(driver), "john (John Doe)")

    def test_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="ABC12345",
        )
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")


class CarModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        car = Car.objects.create(
            model="Model S", manufacturer=manufacturer
        )
        self.assertEqual(str(car), "Model S")
