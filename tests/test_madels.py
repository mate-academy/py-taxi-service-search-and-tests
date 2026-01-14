from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(manufacturers.values_list("name", flat=True)), ["Audi", "BMW", "Toyota"])


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "driver1 (John Doe)")

    def test_driver_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), f"/drivers/{self.driver.pk}/")


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        self.car = Car.objects.create(model="Model S", manufacturer=self.manufacturer)
        self.driver = get_user_model().objects.create_user(
            username="driver2",
            password="testpass456",
            first_name="Jane",
            last_name="Smith",
            license_number="XYZ98765"
        )
        self.car.drivers.add(self.driver)

    def test_car_str(self):
        self.assertEqual(str(self.car), "Model S")

    def test_car_manufacturer_relationship(self):
        self.assertEqual(self.car.manufacturer, self.manufacturer)

    def test_car_driver_relationship(self):
        self.assertIn(self.driver, self.car.drivers.all())
