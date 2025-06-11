from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Manufacturer, Car


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="test",
            password="test123",
            license_number="TES12345",
        )

    def test_create_driver(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.username, "test")
        self.assertTrue(driver.check_password("test123"))
        self.assertEqual(driver.license_number, "TES12345")

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        expected_str = (f"{driver.username} "
                        f"({driver.first_name} {driver.last_name})")
        self.assertEqual(str(driver), expected_str)

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        expected = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected)


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

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_str = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_str)


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="test",
            password="test123",
            license_number="TES12345",
        )

        test_manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )

        test_car = Car.objects.create(
            model="test_model",
            manufacturer=test_manufacturer,
        )
        drivers = Driver.objects.all()
        test_car.drivers.set(drivers)
        test_car.save()

    def test_create_car(self):
        car = Car.objects.get(id=1)
        manufacturer = car.manufacturer
        drivers = Driver.objects.all()
        self.assertEqual(car.model, "test_model")
        self.assertEqual(car.manufacturer, manufacturer)
        self.assertEqual(list(car.drivers.all()), list(drivers))

    def test_car_str(self):
        car = Car.objects.get(id=1)
        expected_str = f"{car.model}"
        self.assertEqual(str(car), expected_str)
