from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ModelsTest(TestCase):
    def setUp(self) -> None:

        self.driver = Driver.objects.create_user(
            username="Test username",
            license_number="TES45678",
            first_name="Test name",
            last_name="Test surname"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="1 Test manufacturer name",
            country="Test manufacturer country"
        )
        self.manufacture_2 = Manufacturer.objects.create(
            name="2 Test manufacturer name",
            country="Test manufacturer country"
        )
        self.manufacture_3 = Manufacturer.objects.create(
            name="3 Test manufacturer name",
            country="Test manufacturer country"
        )
        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="Test car model"
        )
        self.car.drivers.add(self.driver)

    def test_manufacturer_fields_correct(self):
        self.assertEqual(
            self.manufacturer.name,
            "1 Test manufacturer name"
        )
        self.assertEqual(
            self.manufacturer.country,
            "Test manufacturer country"
        )

    def test_manufacturer_str_correct(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_manufacturer_ordering_correct(self):
        self.assertEqual(
            [
                self.manufacturer,
                self.manufacture_2,
                self.manufacture_3
            ],
            list(Manufacturer.objects.all())
        )

    def test_car_str_correct(self):
        self.assertEqual(
            str(self.car),
            self.car.model
        )

    def test_car_fields_correct(self):
        self.assertEqual(self.car.model, "Test car model")
        self.assertEqual(self.car.manufacturer, self.manufacturer)
        self.assertIn(self.driver, self.car.drivers.all())

    def test_driver_license_number_correct(self):
        self.assertEqual(self.driver.license_number, "TES45678")

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        )
