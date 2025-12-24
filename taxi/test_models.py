from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="<NAME>",
            country="<COUNTRY>",
        )
        self.driver = Driver.objects.create(
            username="<USERNAME>",
            password="<<PASSWORD>>",
            license_number="ERS12345"
        )
        self.car = Car.objects.create(
            model="<MODEL>",
            manufacturer=self.manufacturer,
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username}"
            f" ({self.driver.first_name}"
            f" {self.driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        link = self.driver.get_absolute_url()
        self.assertEqual(
            reverse("taxi:driver-detail",
                    kwargs={"pk": self.driver.id}), link
        )

    def test_car_str(self):
        self.car.drivers.add(self.driver)
        self.car.save()
        self.assertEqual(str(self.car), self.car.model)
