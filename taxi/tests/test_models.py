from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            username="test",
            password="test12345",
            license_number="AAA11111",
            first_name="TestFirstName",
            last_name="TestLastName")

    def test_username_label(self):
        driver = Driver.objects.get(id=1)
        field_label = driver._meta.get_field("username").verbose_name
        self.assertEqual(field_label, "username")

    def test_password_label(self):
        driver = Driver.objects.get(id=1)
        field_label = driver._meta.get_field("password").verbose_name
        self.assertEqual(field_label, "password")

    def test_license_number_label(self):
        driver = Driver.objects.get(id=1)
        field_label = driver._meta.get_field("license_number").verbose_name
        self.assertEqual(field_label, "license number")

    def test_first_name_label(self):
        driver = Driver.objects.get(id=1)
        field_label = driver._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_last_name_label(self):
        driver = Driver.objects.get(id=1)
        field_label = driver._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_license_number_max_length(self):
        driver = Driver.objects.get(id=1)
        max_length = driver._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 255)

    def test_driver_str(self):
        driver = Driver.objects.get(id=1)
        expected_object_name = f"{driver.username} ({driver.first_name} {driver.last_name})"
        self.assertEqual(str(driver), expected_object_name)

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry")

        Car.objects.create(
            model="TestModel",
            manufacturer=manufacturer)

    def test_model_label(self):
        car = Car.objects.get(id=1)
        field_label = car._meta.get_field("model").verbose_name
        self.assertEqual(field_label, "model")

    def test_manufacturer_label(self):
        car = Car.objects.get(id=1)
        field_label = car._meta.get_field("manufacturer").verbose_name
        self.assertEqual(field_label, "manufacturer")

    def test_drivers_label(self):
        car = Car.objects.get(id=1)
        field_label = car._meta.get_field("drivers").verbose_name
        self.assertEqual(field_label, "drivers")

    def test_model_max_length(self):
        car = Car.objects.get(id=1)
        max_length = car._meta.get_field("model").max_length
        self.assertEqual(max_length, 255)

    def test_car_str(self):
        car = Car.objects.get(id=1)
        expected_object_name = f"{car.model}"
        self.assertEqual(str(car), expected_object_name)


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(
            name="TestName",
            country="TestCountry")

    def test_name_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_country_label(self):
        manufacturer = Manufacturer.objects.get(id=1)
        field_label = manufacturer._meta.get_field("country").verbose_name
        self.assertEqual(field_label, "country")

    def test_name_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_country_max_length(self):
        manufacturer = Manufacturer.objects.get(id=1)
        max_length = manufacturer._meta.get_field("country").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEqual(str(manufacturer), expected_object_name)

    def test_manufacturer_ordering(self):
        manufacturer = Manufacturer.objects.get(id=1)
        ordering = manufacturer._meta.ordering
        self.assertEquals(ordering[0], "name")
