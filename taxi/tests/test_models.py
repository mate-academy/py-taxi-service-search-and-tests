from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self):
        manufacturer_list = {
            ("Suzuki", "Japan"),
            ("Kia", "South Korea"),
            ("Audi", "Germany")
        }
        for manufacturer in manufacturer_list:
            name, country = manufacturer
            Manufacturer.objects.create(
                name=name,
                country=country
            )

        self.manufacturer = Manufacturer.objects.get(name="Suzuki")

        self.driver = get_user_model().objects.create_user(
            username="test-name",
            password="test12345",
            first_name="Firstname",
            last_name="Lastname",
            license_number="XXX12345"
        )

        self.car = Car.objects.create(
            model="test-model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_manufacturer_ordering(self):
        self.assertEqual(
            [man.name for man in Manufacturer.objects.all()],
            ["Audi", "Kia", "Suzuki"]
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name} {self.driver.last_name})"
        )

    def test_driver_license_number_field(self):
        self.assertEqual(self.driver.license_number, "XXX12345")

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_car_fields(self):
        self.car.drivers.add(self.driver)

        self.assertEqual(
            (self.car.model,
             self.car.manufacturer.name,
             self.car.drivers.get(username="test-name").username,
             ),
            ("test-model", "Suzuki", "test-name")
        )
