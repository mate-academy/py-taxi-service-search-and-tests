from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.manufacturer = Manufacturer.objects.create(
            name="manufacturer1",
            country="country1",
        )
        cls.driver = get_user_model().objects.create_user(
            username="driver1",
            password="test12345",
            first_name="first_name1",
            last_name="last_name1",
            license_number="AAA12345"
        )
        cls.car = Car.objects.create(
            model="model1",
            manufacturer=cls.manufacturer,
        )
        cls.car.drivers.add(cls.driver)

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
            msg="Manufacturer string representation is incorrect"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            (f"{self.driver.username} ({self.driver.first_name} "
             f"{self.driver.last_name})"),
            msg="Driver string representation is incorrect"
        )

    def test_car_str(self):
        self.assertEqual(
            str(self.car),
            self.car.model,
            msg="Car string representation is incorrect"
        )

    def test_car_has_driver(self):
        self.assertIn(
            self.driver,
            self.car.drivers.all(),
            msg=(
                f"The car {self.car.model} "
                f"should have driver {self.driver.username}"
            )
        )

    def test_driver_license_number_created(self):
        self.assertEqual(
            self.driver.license_number,
            "AAA12345",
            msg="Driver license number is incorrect"
        )

    def test_driver_password(self):
        self.assertTrue(
            self.driver.check_password("test12345"),
            msg="Driver password check failed"
        )
