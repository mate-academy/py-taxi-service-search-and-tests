from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTests(TestCase):
    def test_manufacturer_str(self):
        test_manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        self.assertEqual(
            str(test_manufacturer),
            f"{test_manufacturer.name} {test_manufacturer.country}")

    def test_manufacturer_name(self):
        man_name = "test_manufacturer"
        manufacturer_name = Manufacturer.objects.create(name=man_name)
        self.assertEqual(manufacturer_name.name, man_name)


class DriverModelTests(TestCase):
    def test_driver_str(self):
        test_driver = Driver.objects.create(
            username="test_driver",
            first_name="test_first_name",
            last_name="test_last_name")
        self.assertEqual(
            str(test_driver),
            f"{test_driver.username}"
            f" ({test_driver.first_name} {test_driver.last_name})"
        )

    def test_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)


class CarModelTests(TestCase):
    def test_car_drivers(self):
        test_driver1 = Driver.objects.create(
            username="test_driver1",
            license_number="ABC12345")
        test_driver2 = Driver.objects.create(
            username="test_driver2",
            license_number="ZXC12345")
        test_manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country")

        car = Car.objects.create(model="BMW", manufacturer=test_manufacturer)

        # Назначаем водителей через ManyToMany
        car.drivers.set([test_driver1, test_driver2])

        self.assertEqual(car.drivers.count(), 2)
        self.assertEqual(car.model, "BMW")
        self.assertEqual(car.manufacturer, test_manufacturer)
        self.assertIn(test_driver1, car.drivers.all())
        self.assertIn(test_driver2, car.drivers.all())
