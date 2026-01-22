from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase

from taxi.models import Manufacturer, Car

Driver = get_user_model()

MANUFACTURERS = [
    {"name": "A_manufacturer", "country": "Country1"},
    {"name": "C_manufacturer", "country": "Country2"},
    {"name": "B_manufacturer", "country": "Country3"}
]


class ManufactureModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.bulk_create(
            map(
                lambda manufacturer: Manufacturer(**manufacturer),
                MANUFACTURERS
            )
        )

    def test_name_label(self):
        manufacturer = Manufacturer.objects.get(pk=1)
        field_label = manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_country_label(self):
        manufacturer = Manufacturer.objects.get(pk=1)
        field_label = manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")

    def test_name_max_length(self):
        manufacturer = Manufacturer.objects.get(pk=1)
        max_length = manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_country_max_length(self):
        manufacturer = Manufacturer.objects.get(pk=1)
        max_length = manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)

    def test_name_unique(self):
        manufacturer = Manufacturer.objects.get(pk=1)
        unique = manufacturer._meta.get_field("name").unique
        self.assertTrue(unique)

    def test_default_ordering_by_name(self):
        self.assertEqual(
            list(Manufacturer.objects.order_by("name")),
            list(Manufacturer.objects.all())
        )

    def test_object_name(self):
        manufacturer = Manufacturer.objects.get(pk=1)
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last",
            license_number="AAA12345"
        )

    def test_license_number_label(self):
        driver = Driver.objects.get(pk=1)
        field_label = driver._meta.get_field("license_number").verbose_name
        self.assertEqual(field_label, "license number")

    def test_license_number_max_length(self):
        driver = Driver.objects.get(pk=1)
        max_length = driver._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 255)

    def test_license_number_unique(self):
        driver = Driver.objects.get(pk=1)
        unique = driver._meta.get_field("license_number").unique
        self.assertTrue(unique)

    def test_driver_verbose_names(self):
        driver = Driver.objects.get(pk=1)
        verbose_name = driver._meta.verbose_name
        verbose_name_plural = driver._meta.verbose_name_plural
        self.assertEqual(verbose_name, "driver")
        self.assertEqual(verbose_name_plural, "drivers")

    def test_object_name(self):
        driver = Driver.objects.get(pk=1)
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = Driver.objects.get(pk=1)
        self.assertEqual(
            driver.get_absolute_url(),
            "/drivers/1/"
        )


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            **MANUFACTURERS[0]
        )

        Car.objects.create(
            model="A_model",
            manufacturer=manufacturer,
        )

    def test_model_max_length(self):
        car = Car.objects.get(pk=1)
        max_length = car._meta.get_field("model").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer(self):
        car = Car.objects.get(pk=1)

        field = car._meta.get_field("manufacturer")

        label = field.verbose_name
        self.assertEqual(label, "manufacturer")

        many_to_one = field.many_to_one
        self.assertTrue(many_to_one)

        on_delete = field.remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

        model = field.remote_field.model
        self.assertEqual(model, Manufacturer)

    def test_drivers(self):
        car = Car.objects.get(pk=1)

        field = car._meta.get_field("drivers")

        label = field.verbose_name
        self.assertEqual(label, "drivers")

        many_to_many = field.many_to_many
        self.assertTrue(many_to_many)

        model = field.remote_field.model
        self.assertEqual(model, Driver)

        related_name = field._related_name
        self.assertEqual(related_name, "cars")

    def test_object_name(self):
        car = Car.objects.get(pk=1)
        self.assertEqual(
            str(car),
            car.model
        )
