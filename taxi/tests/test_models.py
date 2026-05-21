from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            license_number="XYZ12345"
        )

    def test_str_method(self):
        expected_str = (
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )
        self.assertEqual(str(self.driver), expected_str)

    def test_driver_fields(self):
        self.assertEqual(self.driver.username, "johndoe")
        self.assertEqual(self.driver.first_name, "John")
        self.assertEqual(self.driver.last_name, "Doe")
        self.assertEqual(self.driver.license_number, "XYZ12345")

    def test_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)


class ManufacturerModelTest(TestCase):
    def test_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        expected_str = "Tesla USA"
        self.assertEqual(str(manufacturer), expected_str)

    def test_manufacturer_ordering(self):
        m_audi = Manufacturer.objects.create(name="Audi", country="Germany")
        m_bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        m_alfa = Manufacturer.objects.create(
            name="Alfa Romeo",
            country="Italy"
        )

        manufacturers = list(Manufacturer.objects.all())

        expected_order = [m_alfa, m_audi, m_bmw]
        self.assertEqual(manufacturers, expected_order)


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_str_method(self):
        car = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer
        )
        self.assertEqual(str(car), "Mustang")

    def test_car_manufacturer_relation(self):
        car = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer
        )

        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertIn(car, self.manufacturer.car_set.all())
