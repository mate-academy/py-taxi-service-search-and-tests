from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="Manufacturer C", country="Country C")
        Manufacturer.objects.create(name="Manufacturer B", country="Country B")
        Manufacturer.objects.create(name="Manufacturer A", country="Country A")
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(manufacturers[0].name, "BMW")
        self.assertEqual(manufacturers[1].name, "Manufacturer A")
        self.assertEqual(manufacturers[2].name, "Manufacturer B")
        self.assertEqual(manufacturers[3].name, "Manufacturer C")

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "BMW Germany")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            license_number="ABC12345",
            first_name="Test",
            last_name="Test",
        )
        self.assertEqual(str(driver), "testuser (Test Test)")

    def test_car_str(self):
        car = Car.objects.create(
            model="X5", manufacturer=self.manufacturer
        )
        self.assertEqual(str(car), "X5")
