from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.license_number = "ABC12345"
        self.driver = get_user_model().objects.create_user(
            username="driver_GH",
            password="Dri#$^ver_22#$34_pas^#%s_54@#22",
            first_name="Serejka",
            last_name="Senior",
            license_number=self.license_number,
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Ukraine"
        )

    def test_manufacturer_str(self):
        str_representation = str(self.manufacturer)
        expected_result = (
            f"{self.manufacturer.name} "
            f"{self.manufacturer.country}"
        )
        self.assertEqual(str_representation, expected_result)

    def test_driver_has_a_license_number(self):
        self.assertEqual(self.driver.license_number, self.license_number)

    def test_driver_str(self):
        expected_result = (
            f"{self.driver.username} ({self.driver.first_name} "
            f"{self.driver.last_name})"
        )
        self.assertEqual(str(self.driver), expected_result)

    def test_car_str(self):
        car = Car.objects.create(
            model="Some_test_model",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)
        expected_result = str(car.model)
        self.assertEqual(expected_result, car.model)
