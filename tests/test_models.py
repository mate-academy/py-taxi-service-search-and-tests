from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_create_manufacturer(self):
        self.assertEqual("Toyota", self.manufacturer.name)
        self.assertEqual("Japan", self.manufacturer.country)

    def test_manufacturer_max_length(self):
        name_max_length = self.manufacturer._meta.get_field(
            "name"
        ).max_length
        country_max_length = self.manufacturer._meta.get_field(
            "country"
        ).max_length

        self.assertEqual(255, name_max_length)
        self.assertEqual(255, country_max_length)

    def test_manufacturer_str(self):
        self.assertEqual(
            f"{self.manufacturer.name} {self.manufacturer.country}",
            str(self.manufacturer)
        )

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            ["Audi", "BMW", "Toyota"],
            list(manufacturers.values_list("name", flat=True))
        )


class DriverModelTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345",
        )

    def test_create_driver(self):
        self.assertEqual("test", self.driver.username)
        self.assertTrue((self.driver.check_password("test123")))
        self.assertEqual("ABC12345", self.driver.license_number)

    def test_license_number_max_length(self):
        license_number_max_length = self.driver._meta.get_field(
            "license_number"
        ).max_length

        self.assertEqual(255, license_number_max_length)

    def test_verbose_name(self):
        self.assertEqual("driver", self.driver._meta.verbose_name)
        self.assertEqual("drivers", self.driver._meta.verbose_name_plural)

    def test_manufacturer_str(self):
        self.assertEqual(
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
            str(self.driver)
        )

    def test_get_absolute_url(self):
        self.assertEqual("/drivers/1/", self.driver.get_absolute_url())


class CarModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="Toyota Camry",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

        self.car = Car.objects.get(pk=self.car.pk)

    def test_create_car(self):
        self.assertEqual(
            self.car.model,
            "Toyota Camry"
        )
        self.assertEqual(
            self.car.manufacturer,
            self.manufacturer,
        )
        self.assertIn(
            self.driver,
            self.car.drivers.all()
        )

    def test_model_max_length(self):
        model_max_length = self.car._meta.get_field("model").max_length

        self.assertEqual(255, model_max_length)

    def test_car_str(self):
        self.assertEqual(self.car.model, str(self.car))

    def test_manufacturer_relationship(self):
        self.assertEqual(self.car.manufacturer, self.manufacturer)

    def test_driver_relationship(self):
        self.assertIn(self.driver, self.car.drivers.all())
        self.assertIn(self.car, self.driver.cars.all())
