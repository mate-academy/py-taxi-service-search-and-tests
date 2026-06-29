from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}",
        )

    def test_driver_str(self) -> None:
        username = "test_username"
        first_name = "test_first_name"
        last_name = "test_last_name"
        password = "pass12345"
        license_number = "AA1111BB"

        driver = get_user_model().objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(
            str(driver),
            f"{username} ({first_name} {last_name})",
        )

    def test_create_driver_with_license_number(self) -> None:
        username = "test_username"
        password = "pass12345"
        license_number = "AX1234BB"

        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(
            driver.license_number,
            license_number,
        )

    def test_driver_get_absolute_url(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="pass12345",
            license_number="AX1234BB",
        )

        self.assertEqual(
            driver.get_absolute_url(),
            f"/drivers/{driver.pk}/",
        )

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )

        self.assertEqual(str(car), car.model)

    def test_car_manufacturer_relation(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )

        self.assertEqual(car.manufacturer, manufacturer)

    def test_car_drivers_many_to_many(self) -> None:
        driver1 = get_user_model().objects.create_user(
            username="test_username1",
            first_name="test_first_name1",
            last_name="test_last_name1",
            password="pass1111",
            license_number="AX1234BB",
        )

        driver2 = get_user_model().objects.create_user(
            username="test_username2",
            first_name="test_first_name2",
            last_name="test_last_name2",
            password="pass2222",
            license_number="BB1234AX",
        )

        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )

        car.drivers.set([driver1, driver2])

        car_drivers = car.drivers.all()

        self.assertEqual(car.drivers.count(), 2)
        self.assertIn(driver1, car_drivers)
        self.assertIn(driver2, car_drivers)

    def test_driver_cars_related_name(self) -> None:
        driver = get_user_model().objects.create_user(
            username="test_username",
            password="pass12345",
            license_number="AA1234BB",
        )

        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )

        car.drivers.add(driver)

        self.assertIn(car, driver.cars.all())
