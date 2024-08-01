from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def setUp(self):
        Manufacturer.objects.bulk_create([
            Manufacturer(name="BB_test", country="country"),
            Manufacturer(name="AA_test", country="country")
        ])
        self.manufacturer = Manufacturer.objects.get(id=1)

        username = "Test_name"
        password = "Test_1234"
        license_number = "ABC12345"
        self.driver = Driver.objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )

        self.car = Car.objects.create(
            model="Test",
            manufacturer=self.manufacturer
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_manufacturers_ordering(self):
        self.assertEqual(
            list(Manufacturer.objects.all()),
            list(Manufacturer.objects.order_by("name"))
        )

    def test_driver_str(self):

        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)
