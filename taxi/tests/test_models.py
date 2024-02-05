from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    """
    TestCase class for testing the models in the taxi app.
    """

    def setUp(self) -> None:
        """
        Set up necessary data for the tests.
        """
        self.license_number = "FTL12345"
        self.driver = get_user_model().objects.create_user(
            username="driver_KLFPW_345",
            password="Dri#$^ver_22#$34_pas^#%s_54@#22",
            first_name="Mykola",
            last_name="Meatball",
            license_number=self.license_number,
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Ukraine"
        )

    def test_manufacturer_str(self):
        """
        Test the string representation of the Manufacturer model.
        """
        str_representation = str(self.manufacturer)
        expected_result = (
            f"{self.manufacturer.name} "
            f"{self.manufacturer.country}"
        )
        self.assertEquals(str_representation, expected_result)

    def test_driver_has_a_license_number(self):
        """
        Test if a driver has the correct license number.
        """
        self.assertEqual(self.driver.license_number, self.license_number)

    def test_driver_str(self):
        """
        Test the string representation of the Driver model.
        """
        expected_result = (
            f"{self.driver.username} ({self.driver.first_name} "
            f"{self.driver.last_name})"
        )
        self.assertEqual(str(self.driver), expected_result)

    def test_car_str(self):
        """
        Test the string representation of the Car model.
        """
        car = Car.objects.create(
            model="Some_test_model",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver)
        expected_result = str(car.model)
        self.assertEquals(expected_result, car.model)
