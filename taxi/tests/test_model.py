from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class TestManufacturer(TestCase):

    def test_manufacturer_create_name_and_country(self):
        """Test that custom columns is correctly added to our model"""
        name = "Volkswagen"
        country = "Germany"
        test_manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )

        self.assertEqual(test_manufacturer.name, name)
        self.assertEqual(test_manufacturer.country, country)

    def test_manufacturer_str(self):
        """Test that dunder method '__str__' of manufacturer
        models is working correctly"""
        name = "Volkswagen"
        country = "Germany"
        test_manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )

        self.assertEqual(str(test_manufacturer), f"{name} {country}")


class TestDriver(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create_user(
            username="mc_petya",
            first_name="Petro",
            last_name="Mostavchyk",
            license_number="MOT63142"
        )

    def test_get_absolute_url(self):
        """Test that we reversed on right address while using
        'get_absolute_url' method"""
        url = self.driver.get_absolute_url()
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )

        self.assertEqual(url, expected_url)


class TestCar(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="test1",
            first_name="Petro",
            last_name="Mostavchyk",
            password="1qazcde3",
            license_number="MOT63132",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="test2",
            first_name="Petro",
            last_name="Mostavchyk",
            password="1qazcde3",
            license_number="MOT63122",
        )

    def test_car_creation(self):
        """Test that car is creation correctly and all drivers
        is assigning in this car"""
        car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.driver1, self.driver2)

        self.assertEqual(car.model, "Test Model")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertIn(self.driver1, car.drivers.all())
        self.assertIn(self.driver2, car.drivers.all())
