from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

TEST = "test"


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name=TEST, country=TEST)
        self.assertEquals(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_create_driver_without_license_number(self):
        user = Driver.objects.create_user(
            username=TEST,
            password=TEST,
            first_name=TEST,
            last_name=TEST,
        )
        self.assertIsNotNone(user)

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username=TEST,
            password=TEST,
            first_name=TEST,
            last_name=TEST,
        )
        self.assertEquals(
            str(driver), f"{driver.username} "
                         f"({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username=TEST,
            password=TEST,
            first_name=TEST,
            last_name=TEST,
        )
        self.assertEquals(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )

    def test_delete_driver(self):
        driver = Driver.objects.create_user(
            username=TEST,
            password=TEST,
            first_name=TEST,
            last_name=TEST,
        )
        driver.delete()
        self.assertIsNone(Driver.objects.filter(username=TEST).first())

    def test_add_driver_to_car(self):
        manufacturer = Manufacturer.objects.create(name=TEST, country=TEST)
        car = Car.objects.create(model=TEST, manufacturer=manufacturer)
        driver = Driver.objects.create_user(
            username=TEST,
            password=TEST,
            first_name=TEST,
            last_name=TEST,
        )
        car.drivers.add(driver)
        self.assertIn(driver, car.drivers.all())

    def test_remove_driver_from_car(self):
        manufacturer = Manufacturer.objects.create(name=TEST, country=TEST)
        car = Car.objects.create(model=TEST, manufacturer=manufacturer)
        driver = Driver.objects.create_user(
            username=TEST,
            password=TEST,
            first_name=TEST,
            last_name=TEST,
        )
        car.drivers.add(driver)
        car.drivers.remove(driver)
        self.assertNotIn(driver, car.drivers.all())

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name=TEST, country=TEST)
        car = Car.objects.create(model=TEST, manufacturer=manufacturer)
        self.assertEquals(str(car), car.model)

    def test_create_car_without_manufacturer(self):
        with self.assertRaises(IntegrityError):
            Car.objects.create(model=TEST)
