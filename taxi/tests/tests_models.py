from django.test import TestCase
from django.db.utils import IntegrityError

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Aname", country="Japan")
        Manufacturer.objects.create(name="Bname", country="Germany")
        Manufacturer.objects.create(name="Cname", country="USA")

    def test_name_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_country_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")

    def test_name_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Manufacturer.objects.create(name="Aname", country="France")

    def test_country_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(str(manufacturer), "Aname Japan")

    def test_manufacturer_ordering_by_name(self):
        manufacturers = list(Manufacturer.objects.all())
        names = [m.name for m in manufacturers]
        self.assertEqual(names, sorted(names))


class CarModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        cls.driver1 = Driver.objects.create_user(
            username="d1", password="pass123", license_number="ASD12345"
        )
        cls.driver2 = Driver.objects.create_user(
            username="d2", password="pass123", license_number="ZXC54321"
        )

    def setUp(self):
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_model_label(self):
        field_label = self.car._meta.get_field("model").verbose_name
        self.assertEqual(field_label, "model")

    def test_model_max_length(self):
        max_length = self.car._meta.get_field("model").max_length
        self.assertEqual(max_length, 255)

    def test_m2m_drivers(self):
        self.car.drivers.add(self.driver1, self.driver2)
        drivers = list(self.car.drivers.all())
        self.assertEqual(drivers, [self.driver1, self.driver2])

        self.car.drivers.remove(self.driver1)
        self.assertNotIn(self.driver1, self.car.drivers.all())


class DriverModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="Driver",
            first_name="TestFirst",
            last_name="TestLast",
            password="test123",
            license_number="ASD12345",
        )

    def test_license_number_is_unique(self):
        with self.assertRaises(IntegrityError):
            Driver.objects.create_user(
                username="Driver1",
                password="test123",
                license_number="ASD12345",
            )

    def test_lisence_number_max_length(self):
        max_length = self.driver._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 255)

    def test_str(self):
        expected = (
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )
        self.assertEqual(str(self.driver), expected)

    def test_get_absolute_url(self):
        excepted_url = f"/drivers/{self.driver.id}/"
        self.assertEqual(self.driver.get_absolute_url(), excepted_url)

    def test_verbose_name(self):
        self.assertEqual(Driver._meta.verbose_name, "driver")

    def test_verbose_name_plural(self):
        self.assertEqual(Driver._meta.verbose_name_plural, "drivers")
