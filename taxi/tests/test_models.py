from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer1 = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="TestManufacturer2",
            country="TestCountry2"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            first_name="Test Name",
            last_name="Test Last Name",
            license_number="ABC012345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="test_username2",
            password="test_password2",
            first_name="Test Name2",
            last_name="Test Last Name2",
            license_number="DBC012345"
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer1,
        )
        self.car.drivers.add(self.driver1, self.driver2)

    def test_manufacturer1_str_method(self) -> None:
        expected_result = "TestManufacturer TestCountry"
        self.assertEquals(str(self.manufacturer1), expected_result)

    def test_manufacturer2_str_method(self) -> None:
        expected_result = "TestManufacturer2 TestCountry2"
        self.assertEquals(str(self.manufacturer2), expected_result)

    def test_driver1_str_method(self) -> None:
        expected_result = "test_username (Test Name Test Last Name)"
        self.assertEquals(str(self.driver1), expected_result)

    def test_driver2_str_method(self) -> None:
        expected_result = "test_username2 (Test Name2 Test Last Name2)"
        self.assertEquals(str(self.driver2), expected_result)

    def test_car_str_method(self) -> None:
        expected_result = self.car.model
        self.assertEquals(str(self.car), expected_result)
