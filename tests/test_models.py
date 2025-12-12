from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

    def test_manufacturer_fields_titles(self):
        field_label_name = self.manufacturer._meta.get_field(
            "name"
        ).verbose_name
        field_label_country = self.manufacturer._meta.get_field(
            "country"
        ).verbose_name
        self.assertEqual(field_label_name, "name")
        self.assertEqual(field_label_country, "country")

    def test_manufacturer_str_method(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            license_number="TES12345"
        )

    def test_driver_fields_titles(self):
        field_label_license_number = (
            self.driver._meta.get_field(
                "license_number"
            )
        ).verbose_name

        self.assertEqual(field_label_license_number, "license number")

    def test_driver_str_method(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name} "
            f"{self.driver.last_name})"
        )


class CarModelTest(TestCase):
    def setUp(self):
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.create(
                name="test_name",
                country="test_country"
            )
        )
        self.car.drivers.add(
            Driver.objects.create(
                username="test_username",
                first_name="test_first_name",
                last_name="test_last_name",
                license_number="TES12345"
            )
        )
        self.car.save()

    def test_car_fields_titles(self):
        field_label_model = self.car._meta.get_field("model").verbose_name
        field_label_manufacturer = self.car._meta.get_field(
            "manufacturer"
        ).verbose_name
        field_label_drivers = self.car._meta.get_field("drivers").verbose_name
        self.assertEqual(field_label_model, "model")
        self.assertEqual(field_label_manufacturer, "manufacturer")
        self.assertEqual(field_label_drivers, "drivers")

    def test_car_str_method(self):
        self.assertEqual(str(self.car), self.car.model)
