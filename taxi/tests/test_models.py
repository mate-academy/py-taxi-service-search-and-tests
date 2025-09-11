from django.db import IntegrityError
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="Ukraine"
        )

    def setUp(self):
        self.manufacturer = Manufacturer.objects.get(pk=1)

    def test_label_of_name(self):
        name_label = self.manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(name_label, "name")

    def test_label_of_country(self):
        country_label = self.manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(country_label, "country")

    def test_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Manufacturer.objects.create(
                name="TestName",
                country="UK"
            )

    def test_max_length_of_name(self):
        name_length = self.manufacturer._meta.get_field("name").max_length
        self.assertEqual(name_length, 255)

    def test_max_length_of_country(self):
        country_length = self.manufacturer._meta.get_field("country").max_length
        self.assertEqual(country_length, 255)

    def test_object_str_is_name_and_country(self):
        f_str = (f"{self.manufacturer.name} "
                 f"{self.manufacturer.country}")
        self.assertEqual(f_str, "TestName Ukraine")


class DriverModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            username="user123",
            first_name="Ivan",
            last_name="Ivanov",
            license_number="ABF23454"
        )

    def setUp(self):
        self.driver = Driver.objects.get(pk=1)

    def test_label_of_license_number(self):
        license_label = self.driver._meta.get_field("license_number").verbose_name
        self.assertEqual(license_label, "license number")

    def test_max_length_of_license_number(self):
        license_max = self.driver._meta.get_field("license_number").max_length
        self.assertEqual(license_max, 255)

    def test_str_name_of_driver(self):
        str_name = (f"{self.driver.username} "
                    f"({self.driver.first_name} "
                    f"{self.driver.last_name})")
        self.assertEqual(str_name, "user123 (Ivan Ivanov)")

    def test_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            "/drivers/1/"
        )


class CarModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="UK"
        )
        cls.driver1 = Driver.objects.create(
            username="user12",
            first_name="Ivan",
            last_name="Ivanov",
            license_number="ACF22222"
        )
        cls.driver2 = Driver.objects.create(
            username="user13",
            first_name="Andriy",
            last_name="Andriev",
            license_number="ACD22122"
        )
        cls.car = Car.objects.create(
            model="TestModel",
            manufacturer=cls.manufacturer
        )
        cls.car.drivers.add(cls.driver1, cls.driver2)

    def test_label_of_model(self):
        model_label = self.car._meta.get_field("model").verbose_name
        self.assertEqual(model_label, "model")

    def test_max_length_of_model(self):
        model_length = self.car._meta.get_field("model").max_length
        self.assertEqual(model_length, 255)

    def test_cascade_deleting(self):
        self.manufacturer.delete()
        cars = Car.objects.all()
        self.assertEqual(cars.count(), 0)

    def test_str_name_of_car(self):
        str_name = self.car.model
        self.assertEqual(str_name, "TestModel")
