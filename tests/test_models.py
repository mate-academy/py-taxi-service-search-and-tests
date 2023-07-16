from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    name = "test_name"
    country = "test_country"

    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name=cls.name, country=cls.country)

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)

        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    username = "test_username"
    first_name = "test_firstname"
    last_name = "test_lastname"
    password = "test_password123"
    license_number = "ANT12345"

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create(
            username=cls.username,
            first_name=cls.first_name,
            last_name=cls.last_name,
            password=cls.password,
            license_number=cls.license_number
        )

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.license_number, DriverModelTest.license_number)

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEquals(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        )

    def test_model_verbose_name(self):
        model_verbose_name = "driver"
        model_verbose_name_plural = "drivers"

        self.assertEqual(
            get_user_model()._meta.verbose_name,
            model_verbose_name
        )
        self.assertEqual(
            get_user_model()._meta.verbose_name_plural,
            model_verbose_name_plural
        )

    def test_driver_str(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(driver),
            f"{DriverModelTest.username} "
            f"({DriverModelTest.first_name} {DriverModelTest.last_name})"
        )


class CarModelTest(TestCase):
    model = "test_model"

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name=ManufacturerModelTest.name,
            country=ManufacturerModelTest.country
        )
        driver_1 = get_user_model().objects.create(
            username=DriverModelTest.username,
            first_name=DriverModelTest.first_name,
            last_name=DriverModelTest.last_name,
            password=DriverModelTest.password,
            license_number=DriverModelTest.license_number
        )

        car = Car.objects.create(
            model=CarModelTest.model,
            manufacturer=manufacturer
        )
        car.drivers.add(driver_1)
        car.save()

    def test_car_str(self):
        car = Car.objects.get(id=1)

        self.assertEqual(
            str(car),
            CarModelTest.model
        )
