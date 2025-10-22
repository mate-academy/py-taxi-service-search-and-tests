from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Test name", country="Test country")
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="password",
            first_name="first",
            last_name="last",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="Test model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def tearDown(self):
        del self.manufacturer
        del self.driver
        del self.car

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_manufacturer_ordering(self):
        manufacturer1 = Manufacturer.objects.create(name="Test name 1", country="Test country 1")
        manufacturer3 = Manufacturer.objects.create(name="Test name 3", country="Test country 2")
        manufacturer2 = Manufacturer.objects.create(name="Test name 2", country="Test country 3")
        self.assertListEqual(
            list(Manufacturer.objects.all()),
            [self.manufacturer, manufacturer1, manufacturer2, manufacturer3],
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} {self.driver.last_name})",
        )

    def test_driver_license_number_exists(self):
        self.assertEqual(
            self.driver.license_number,
            "ABC12345",
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(self.driver.get_absolute_url(), f"/drivers/{self.driver.pk}/")

    def test_car_str(self):
        self.assertEqual(
            str(self.car),
            self.car.model,
        )