from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name="Tesla",
                                                       country="USA")
        cls.driver = Driver.objects.create_user(
            username="John123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )
        cls.car = Car.objects.create(model="Model S",
                                     manufacturer=cls.manufacturer)
        cls.car.drivers.add(cls.driver)

    def test_car_string_representation(self):
        self.assertEqual(str(self.car), "Model S")

    def test_driver_string_representation(self):
        self.assertEqual(str(self.driver), "John123 (John Doe)")

    def test_manufacturer_string_representation(self):
        self.assertEqual(str(self.manufacturer), "Tesla USA")

    def test_driver_absolute_url(self):
        actual_url = self.driver.get_absolute_url()
        expected_url = reverse("taxi:driver-detail",
                               kwargs={"pk": self.driver.pk})
        self.assertEqual(actual_url, expected_url)
