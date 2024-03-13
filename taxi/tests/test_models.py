from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ManufacturerTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_Manufacturer", country="test_Country"
        )
        self.driver = Driver.objects.create_user(
            username="Anton", password="tiguti26", license_number="NO55555"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_label_fields(self):
        fields_list = ["name", "country"]
        for field in fields_list:
            fields_label_check = self.manufacturer._meta.get_field(
                field).verbose_name
            self.assertEqual(fields_label_check, field)
            manufacturer_field_max_length = self.manufacturer._meta.get_field(
                field
            ).max_length
            self.assertEqual(manufacturer_field_max_length, 255)


class DriverTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="Anton", password="tiguti26", license_number="NO55555"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name} "
            f"{self.driver.last_name})",
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")

    def test_label_fields(self):
        fields_label_check = self.driver._meta.get_field(
            "license_number").verbose_name
        self.assertEqual(fields_label_check, "license number")
        driver_field_max_length = self.driver._meta.get_field(
            "license_number"
        ).max_length
        self.assertEqual(driver_field_max_length, 255)


class CarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_Manufacturer", country="test_Country"
        )
        self.driver = driver = Driver.objects.create_user(
            username="Anton", password="tiguti26", license_number="NO55555"
        )
        self.car = Car.objects.create(
            model="test_Model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(driver)

    def test_car(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_label_fields(self):
        fields_list = ["model", "manufacturer", "drivers"]
        for field in fields_list:
            fields_label_check = self.car._meta.get_field(field).verbose_name
            self.assertEqual(fields_label_check, field)
        car_field_max_length = self.car._meta.get_field("model").max_length
        self.assertEqual(car_field_max_length, 255)
