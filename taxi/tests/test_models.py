from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturers = [
            Manufacturer.objects.create(name=name, country="Germany")
            for name in ["BMW", "Audi", "Mercedes"]
        ]
        cls.username = "test_driver"
        cls.password = "test123"
        cls.first_name = "John test"
        cls.last_name = "Doe test"
        cls.license_number = "ABC1234 test"
        cls.driver = get_user_model().objects.create_user(
            username=cls.username,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
            license_number=cls.license_number,
        )
        cls.model = "toyota test"
        cls.car = Car.objects.create(
            model=cls.model,
            manufacturer=cls.manufacturers[0]
        )

    def test_manufacturer_creation(self):
        for manufacturer in self.manufacturers:
            self.assertIsInstance(manufacturer, Manufacturer)
            self.assertIn(
                manufacturer.name,
                ["BMW", "Audi", "Mercedes"])
            self.assertEqual(manufacturer.country, "Germany")

    def test_manufacturer_ordering(self):
        expected_order = sorted(m.name for m in self.manufacturers)
        actual_order = list(Manufacturer.objects.values_list(
            "name",
            flat=True
        ))
        self.assertEqual(actual_order, expected_order)

    def test_manufacturer_str(self):
        for manufacturer in self.manufacturers:
            self.assertEqual(
                str(manufacturer),
                f"{manufacturer.name} {manufacturer.country}"
            )

    def test_driver_creation_with_license_number(self):
        self.assertEqual(self.driver.username, self.username)
        self.assertTrue(self.driver.check_password(self.password))
        self.assertEqual(self.driver.first_name, self.first_name)
        self.assertEqual(self.driver.last_name, self.last_name)
        self.assertEqual(self.driver.license_number, self.license_number)

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.username} ({self.first_name} {self.last_name})"
        )

    def test_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail",
            kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)

    def test_car_creation(self):
        driver2 = get_user_model().objects.create_user(
            username="test2_driver",
            password="test2123",
            first_name="John test2",
            last_name="Doe test2",
            license_number="ABC1234 test2",
        )
        self.car.drivers.set([self.driver, driver2])
        self.assertEqual(self.car.model, self.model)
        self.assertEqual(self.car.manufacturer, self.manufacturers[0])
        self.assertEqual(
            list(self.car.drivers.all()),
            [self.driver, driver2]
        )
