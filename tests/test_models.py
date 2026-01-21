from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class CarModelTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="test model", country="test country"
        )
        Car.objects.create(model="test model", manufacturer=manufacturer)

    def test_str(self):
        car = Car.objects.first()
        self.assertEqual(str(car), "test model")


class DriverModelTest(TestCase):
    USERNAME = "testuser"
    PASSWORD = "qwe12G$z_R"
    FIRST_NAME = "Testjohn"
    LAST_NAME = "Testjohnson"
    LICENSE_NUMBER = "ADD456431"

    def setUp(self):
        Driver.objects.create_user(
            username=self.USERNAME,
            password=self.PASSWORD,
            first_name=self.FIRST_NAME,
            last_name=self.LAST_NAME,
            license_number=self.LICENSE_NUMBER,
        )

    def test_str(self):
        self.assertEqual(
            str(Driver.objects.first()),
            f"{self.USERNAME} ({self.FIRST_NAME} {self.LAST_NAME})"
        )

    def test_license_number(self):
        self.assertEqual(
            Driver.objects.first().license_number, self.LICENSE_NUMBER
        )

    def test_model_verbose_name(self):
        verbose_name = "driver"
        verbose_name_plural = "drivers"
        self.assertEqual(Driver._meta.verbose_name, verbose_name)
        self.assertEqual(Driver._meta.verbose_name_plural, verbose_name_plural)


class ManufacturerModelTest(TestCase):
    INITIAL_DATA = [
        (
            f"{prefix}_name",
            f"{prefix}_country"
        ) for prefix in ["c", "x", "e", "a"]
    ]

    def setUp(self):
        for name, country in self.INITIAL_DATA:
            Manufacturer.objects.create(name=name, country=country)

    def test_str(self):
        manufacturer = Manufacturer.objects.first()
        self.assertEqual(
            str(manufacturer), "a_name a_country"
        )

    def test_ordering(self):
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(manufacturers.values_list("name", "country")),
            [item for item in sorted(self.INITIAL_DATA)]
        )
