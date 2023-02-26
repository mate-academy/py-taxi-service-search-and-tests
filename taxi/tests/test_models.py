from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ModelManufacturerTests(TestCase):
    def test_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestMark",
            country="Antarctica"
        )
        self.assertEqual(
            manufacturer.__str__(),
            f"{manufacturer.name} {manufacturer.country}"
        )


class ModelDriverTests(TestCase):
    def setUp(self):
        self.license_number_ = "AVD12345"
        self.driver_ = Driver.objects.create_user(
            license_number=self.license_number_,
            username="TestDriver",
            password="qwerty123driver",
            last_name="Testa",
            first_name="Testov"
        )

    def test_license_number(self):
        self.assertEqual(self.driver_.license_number, self.license_number_)

    def test_str(self):
        self.assertEqual(
            self.driver_.__str__(),
            f"{self.driver_.username} "
            f"({self.driver_.first_name} {self.driver_.last_name})")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.driver_.get_absolute_url(),
            f"/drivers/{self.driver_.id}/"
        )


class ModelCarTests(TestCase):
    def test_str(self):
        manufacturer_ = Manufacturer.objects.create(
            name="Test",
            country="Antarctica"
        )

        car = Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer_
        )
        self.assertEqual(car.__str__(), car.model)
