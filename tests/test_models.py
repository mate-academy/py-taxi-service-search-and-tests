from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer(name="Manufacturer", country="UA")
        self.assertEqual(str(manufacturer), "Manufacturer UA")

    def test_car_str(self):
        manufacturer = Manufacturer(name="Manufacturer", country="UA")
        car = Car(model="BMW", manufacturer=manufacturer)
        self.assertEqual(str(car), "BMW")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="test_driver",
            password="12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )

        self.assertEqual(str(driver), "test_driver (John Doe)")

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )
