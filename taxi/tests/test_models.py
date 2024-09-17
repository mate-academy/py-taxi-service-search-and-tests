from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="MAN INC", country="Germany")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEquals(str(manufacturer), expected_object_name)


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="john11",
            first_name="John",
            last_name="Doe",
            password="111222John",
            license_number="ADM56984",
        )

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)
        expected_object_name = (
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertEquals(str(driver), expected_object_name)

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.get(id=1)
        username = "john11"
        first_name = "John"
        last_name = "Doe"
        password = "111222John"
        license_number = "ADM56984"

        self.assertEquals(driver.username, username)
        self.assertEquals(driver.first_name, first_name)
        self.assertEquals(driver.last_name, last_name)
        self.assertTrue(driver.check_password(password))
        self.assertEquals(driver.license_number, license_number)

    def test_get_absolute_url(self):
        author = get_user_model().objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), "/drivers/1/")


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="MAN INC",
            country="Germany"
        )

        driver1 = get_user_model().objects.create_user(
            username="john11",
            first_name="John",
            last_name="Doe",
            password="111222John",
            license_number="ADM56984",
        )

        driver2 = get_user_model().objects.create_user(
            username="vlad1",
            first_name="Vlad",
            last_name="Shatrovskyi",
            password="111222Vlad",
            license_number="MIK25131",
        )

        car = Car.objects.create(
            model="BMW",
            manufacturer=manufacturer,
        )

        car.drivers.add(driver1, driver2)
        car.save()

    def test_car_str(self):
        car = Car.objects.get(id=1)
        expected_object_name = car.model
        self.assertEquals(str(car), expected_object_name)
