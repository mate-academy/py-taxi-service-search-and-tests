from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Manufacturer, Car


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create(
            username="TestDr1v3Rr",
            first_name="name",
            last_name="surname",
            license_number="ABC12345"
        )

    def test_to_string(self):
        self.assertEqual(str(self.driver), "TestDr1v3Rr (name surname)")

    def test_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer_a = Manufacturer.objects.create(
            name="A",
            country="testA"
        )
        cls.manufacturer_b = Manufacturer.objects.create(
            name="B",
            country="testB"
        )
        cls.manufacturer_c = Manufacturer.objects.create(
            name="C",
            country="testC"
        )

    def test_ordering_by_name_asc(self):
        manufacturers = Manufacturer.objects.all()
        names = [m.name for m in manufacturers]
        self.assertEqual(names, ["A", "B", "C"])

    def test_to_string(self):
        self.assertEqual(str(self.manufacturer_a), "A testA")


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer_a = Manufacturer.objects.create(
            name="A",
            country="testA"
        )
        cls.car = Car.objects.create(
            model="test_model",
            manufacturer=cls.manufacturer_a
        )

    def test_to_string(self):
        self.assertEqual(str(self.car), "test_model")
