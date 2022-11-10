from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="BMW", country="Germany")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturer_model_labels_and_fields_quantity(self):
        manufacturer = Manufacturer.objects.get(id=1)
        model_fields = [field.name for field in manufacturer._meta.fields]
        expected_fields = ["id", "name", "country"]

        self.assertEqual(model_fields, expected_fields)


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        driver = Driver.objects.create_user(
            username="username1", password="user1234name"
        )
        car = Car.objects.create(model="M3", manufacturer=manufacturer)
        car.drivers.add(driver)

    def test_car_str(self):
        car = Car.objects.get(id=1)

        self.assertEqual(str(car), f"{car.model}")

    def test_car_model_labels_and_fields_quantity(self):
        car = Car.objects.get(id=1)
        model_fields = [field.name for field in car._meta.get_fields()]
        expected_fields = ["id", "model", "manufacturer", "drivers"]

        self.assertEqual(model_fields, expected_fields)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create_user(
            username="test_user",
            password="test12345USER",
            license_number="ABC12345",
            first_name="test",
            last_name="user",
        )

    def test_create_driver_with_license_number(self):
        driver = Driver.objects.get(id=1)
        field_label = driver._meta.get_field("license_number").verbose_name

        self.assertEqual(field_label, "license number")
        self.assertTrue(driver.check_password("test12345USER"))
        self.assertEqual(driver.username, "test_user")

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)

        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
