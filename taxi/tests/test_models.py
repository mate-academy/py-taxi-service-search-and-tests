from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(name="Ford",
                                                         country="USA")
        self.manufacturer2 = Manufacturer.objects.create(name="BMW",
                                                         country="Germany")

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer1), "Ford USA")

    def test_manufacturer_ordering(self):
        self.assertEqual(list(Manufacturer.objects.all()),
                         [self.manufacturer2, self.manufacturer1])


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver_1",
            first_name="Test",
            last_name="Dr",
            license_number="ABC12345",
            email="test@example.com",
            password="Password123",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver), "driver_1 (Test Dr)"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
        )


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="VW",
                                                        country="Germany")
        self.car = Car.objects.create(model="B6",
                                      manufacturer=self.manufacturer)

    def test_str_method(self):
        self.assertEqual(str(self.car), "B6")
