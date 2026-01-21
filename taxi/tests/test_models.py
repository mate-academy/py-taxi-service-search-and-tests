from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Manufacturer, Driver, Car


class TestManufacturerModel(TestCase):
    def setUp(self):
        self.created_manufacturer = Manufacturer.objects.create(
            name="Manufacturer-1",
            country="Country-1",
        )

    def test_manufacturer_creation(self):
        manufacturer = Manufacturer.objects.first()

        self.assertEqual(
            manufacturer.name,
            self.created_manufacturer.name
        )

        self.assertEqual(
            manufacturer.country,
            self.created_manufacturer.country
        )

    def test_manufacturer_str_method(self):
        self.assertTrue(
            str(self.created_manufacturer),
            f"{self.created_manufacturer.name} "
            f"{self.created_manufacturer.country}"
        )


class TestCarModel(TestCase):
    def setUp(self):
        self.created_manufacturer = Manufacturer.objects.create(
            name="Manufacturer-1",
            country="Country-1",
        )

        self.created_drivers = Driver.objects.bulk_create(
            [
                Driver(
                    username="D-1",
                    password="d-1-password",
                    license_number="JIM26531"
                ),
                Driver(
                    username="D-2",
                    password="d-2-password",
                    license_number="DOM26531"
                ),
            ],
        )

        self.model_params = {
            "model": "M-1",
            "manufacturer": self.created_manufacturer,
        }

    def test_driver_creation(self):
        created_car = Car.objects.create(**self.model_params)

        created_car.drivers.set(self.created_drivers)

        self.assertEqual(
            created_car.model,
            self.model_params["model"]
        )
        self.assertEqual(
            created_car.manufacturer,
            self.model_params["manufacturer"]
        )
        self.assertEqual(
            list(created_car.drivers.all()),
            list(self.created_drivers)
        )

    def test_driver_str_method(self):
        created_car = Car.objects.create(**self.model_params)

        self.assertEqual(str(created_car), self.model_params["model"])


class TestDriverModel(TestCase):
    def test_driver_creation(self):
        model_params = {
            "username": "Driver-1",
            "license_number": "JIM26531",
            "first_name": "First",
            "last_name": "Last",
            "password": "user_password",
        }
        created_driver = Driver.objects.create_user(**model_params)

        self.assertEqual(created_driver.username, model_params["username"])
        self.assertEqual(
            created_driver.license_number,
            model_params["license_number"]
        )
        self.assertEqual(created_driver.first_name, model_params["first_name"])
        self.assertEqual(created_driver.last_name, model_params["last_name"])
        self.assertTrue(
            created_driver.check_password(model_params["password"])
        )
