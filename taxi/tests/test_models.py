from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class TestModel(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer(
            name="Test name",
            country="Test Country"
        )

        self.driver = Driver.objects.create(
            username="text.user1",
            password="test123",
            first_name="testname1",
            last_name="testlastname1",
            license_number="12345671",

        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            str(f"{self.manufacturer.name} {self.manufacturer.country}")
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str(self):
        Manufacturer.objects.create(name="TestName", country="TestCountry")
        car = Car.objects.create(
            model="TestModel", manufacturer=Manufacturer.objects.get(id=1)
        )
        self.assertEqual(
            str(car),
            car.model
        )

    def test_check_author_with_license_number(self):
        license_number = self.driver.license_number
        self.assertEqual(self.driver.license_number, license_number)
