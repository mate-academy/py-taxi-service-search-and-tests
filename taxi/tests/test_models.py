from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}"
                         )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test",
            password="test1234",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test1234"
        license_number = "test license_number"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_driver_search_by_username(self):

        Driver.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="jane_doe",
            first_name="Jane",
            last_name="Doe",
            license_number="XYZ98765"
        )

        driver = Driver.objects.get(username="john_doe")
        self.assertEqual(driver.first_name, "John")
        self.assertEqual(driver.last_name, "Doe")

        driver = Driver.objects.get(username="jane_doe")
        self.assertEqual(driver.first_name, "Jane")
        self.assertEqual(driver.last_name, "Doe")

    def test_car_search_by_model(self):

        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="Camry", manufacturer=manufacturer)

        car = Car.objects.get(model="Corolla")
        self.assertEqual(car.manufacturer.name, "Toyota")

        car = Car.objects.get(model="Camry")
        self.assertEqual(car.manufacturer.name, "Toyota")

    def test_manufacturer_search_by_name(self):
        # Создаем производителей
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Honda", country="Japan")

        manufacturer = Manufacturer.objects.get(name="Toyota")
        self.assertEqual(manufacturer.country, "Japan")

        manufacturer = Manufacturer.objects.get(name="Honda")
        self.assertEqual(manufacturer.country, "Japan")
