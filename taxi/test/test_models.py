from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Coco",
            country="USA"
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = Driver.objects.create(
            license_number="AAA55555",
            username="Ruslan15",
            first_name="Ruslan",
            last_name="Topal",
            password="test_Password1",
        )

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Lilit",
            country="Ukraine"
        )

        driver = Driver.objects.create(
            license_number="AAA55555",
            username="Bob25",
            first_name="Bob",
            last_name="Pop",
            password="test_Password1",
        )

        car = Car.objects.create(
            model="KIA",
            manufacturer=manufacturer,
        )

        car.drivers.add(driver)

        self.assertEqual(
            str(car), car.model
        )

    def test_create_driver_with_license_number(self):
        license_number = "AAA11111"
        password = "test_Password1"
        username = "Alin_Wok91"
        first_name = "Alin"
        last_name = "Gray"
        driver = get_user_model().objects.create_user(
            license_number=license_number,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
