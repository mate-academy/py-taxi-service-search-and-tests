from django.test import TestCase

from taxi.models import Manufacturer, Car, Driver


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )

    def test_name_max_length(self):
        manufacturer = Manufacturer.objects.get(name="Test Manufacturer")
        max_length = manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_country_max_length(self):
        manufacturer = Manufacturer.objects.get(name="Test Manufacturer")
        max_length = manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(name="Test Manufacturer")
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_object_name)

    def test_name_unique(self):
        with self.assertRaises(Exception):
            Manufacturer.objects.create(name="Test Manufacturer")


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        cls.car = Car.objects.create(
            model="test model",
            manufacturer=cls.manufacturer,
        )

    def test_name_max_length(self):
        max_length = self.car._meta.get_field("model").max_length
        self.assertEqual(max_length, 255)

    def test_car_str(self):
        expected_object_name = self.car.model
        self.assertEqual(str(self.car), expected_object_name)

    def test_manufacturer_link(self):
        self.assertEqual(self.car.manufacturer.name, "Test Manufacturer")

    def test_many_to_many_drivers(self):
        driver_1 = Driver.objects.create(
            username="username_1",
            first_name="first_name_1",
            last_name="last_name_1",
            email="email_1@email.com",
            license_number="ABC12345",
        )
        driver_2 = Driver.objects.create(
            username="username_2",
            first_name="first_name_2",
            last_name="last_name_2",
            email="email_2@email.com",
            license_number="ABC12346",
        )
        self.car.drivers.add(driver_1, driver_2)

        self.assertIn(driver_1, self.car.drivers.all())
        self.assertIn(driver_2, self.car.drivers.all())
        self.assertEqual(self.car.drivers.count(), 2)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create(
            username="username_1",
            password="<PASSWORD>",
            license_number="ABC12345",
        )

    def test_license_number_max_length(self):
        max_length = self.driver._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 255)

    def test_name_unique(self):
        with self.assertRaises(Exception):
            Driver.objects.create(
                username="username_2",
                password="<PASSWORD_2>",
                license_number="ABC12345",
            )

    def test_license_number_len(self):
        self.assertEqual(len(self.driver.license_number), 8)

    def test_license_number_starts_with_three_upper_letters(self):
        self.assertGreaterEqual(len(self.driver.license_number), 3)
        self.assertTrue(
            self.driver.license_number[:3].isupper(), "Must be uppercase"
        )
        self.assertTrue(
            self.driver.license_number[:3].isalpha(), "Must be letters"
        )

    def test_license_number_ends_with_numbers(self):
        self.assertGreaterEqual(len(self.driver.license_number), 3)
        self.assertTrue(self.driver.license_number[3:].isdigit())

    def test_driver_str_method(self):
        self.assertEqual(
            str(self.driver),
            f""
            f"{self.driver.username} ("
            f"{self.driver.first_name} "
            f"{self.driver.last_name})"
        )
