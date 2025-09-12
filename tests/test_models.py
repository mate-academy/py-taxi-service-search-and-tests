from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.m1 = Manufacturer.objects.create(name="Audi", country="Germany")
        cls.m2 = Manufacturer.objects.create(name="BMW", country="Germany")
        cls.m3 = Manufacturer.objects.create(name="ZAZ", country="Ukraine")

    def test_str(self):
        self.assertEqual(str(self.m1), "Audi Germany")
        self.assertEqual(str(self.m3), "ZAZ Ukraine")

    def test_ordering_by_name(self):
        names = list(Manufacturer.objects.values_list("name", flat=True))
        # ordering = ["name"] => алфавітно
        self.assertEqual(names, sorted(names))

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Manufacturer.objects.create(name="Audi", country="Somewhere")


class DriverModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.driver = cls.User.objects.create_user(
            username="john_doe",
            password="password123",
            first_name="John",
            last_name="Doe",
            license_number="AB123456",
            email="john@example.com",
        )

    def test_meta_verbose_names(self):
        # значення задані в Meta вашої моделі
        self.assertEqual(self.User._meta.verbose_name, "driver")
        self.assertEqual(self.User._meta.verbose_name_plural, "drivers")

    def test_str(self):
        self.assertEqual(str(self.driver), "john_doe (John Doe)")

    def test_get_absolute_url(self):
        expected = reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        self.assertEqual(self.driver.get_absolute_url(), expected)

    def test_unique_license_number(self):
        with self.assertRaises(IntegrityError):
            self.User.objects.create_user(
                username="jane_doe",
                password="password123",
                first_name="Jane",
                last_name="Doe",
                license_number="AB123456",  # дубль
                email="jane@example.com",
            )


class CarModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        cls.User = get_user_model()
        cls.d1 = cls.User.objects.create_user(
            username="a",
            password="x",
            first_name="A",
            last_name="A",
            license_number="LIC23568"
        )
        cls.d2 = cls.User.objects.create_user(
            username="b",
            password="x",
            first_name="B",
            last_name="B",
            license_number="LIC23544"
        )
        cls.car = Car.objects.create(
            model="Corolla",
            manufacturer=cls.manufacturer
        )
        cls.car.drivers.add(cls.d1, cls.d2)

    def test_str(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_manufacturer_fk(self):
        self.assertEqual(self.car.manufacturer.name, "Toyota")

    def test_m2m_drivers_and_related_name(self):
        # через M2M
        self.assertEqual(self.car.drivers.count(), 2)
        self.assertIn(self.car, self.d1.cars.all())  # related_name="cars"
        self.assertIn(self.car, self.d2.cars.all())

    def test_cascade_delete_on_manufacturer(self):
        self.manufacturer.delete()
        self.assertFalse(Car.objects.filter(model="Corolla").exists())
