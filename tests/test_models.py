from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class TestManufactureModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer1 = Manufacturer.objects.create(
            name="Test_name",
            country="Test_Country"
        )
        cls.manufacturer2 = Manufacturer.objects.create(
            name="Best_name",
            country="Test_Country"
        )
        cls.manufacturer3 = Manufacturer.objects.create(
            name="Rest_name",
            country="Test_Country"
        )

    def test_manufacturer_representation(self):
        self.assertEqual(str(self.manufacturer1), "Test_name Test_Country")

    def test_manufacturer_ordering(self):
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(manufacturers), [
            self.manufacturer2,
            self.manufacturer3,
            self.manufacturer1])


class TestDriverModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create(
            username="test_username",
            first_name="Adam",
            last_name="Hefner",
            password="1aadjango1",
            license_number="QWE23435"
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "test_username (Adam Hefner)")

    def test_driver_verbose_name_and_plural(self):
        self.assertEqual(Driver._meta.verbose_name, "driver")
        self.assertEqual(Driver._meta.verbose_name_plural, "drivers")

    def test_driver_get_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail", kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)


class TestCarModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.manufacturer1 = Manufacturer.objects.create(
            name="Test_name",
            country="Test_Country"
        )
        cls.driver = get_user_model().objects.create(
            username="test_username",
            first_name="Adam",
            last_name="Hefner",
            password="1aadjango1",
            license_number="QWE23435"
        )
        cls.car = Car.objects.create(
            model="test_model",
            manufacturer=cls.manufacturer1,
        )
        cls.car.drivers.add(cls.driver)

    def test_car_str(self):
        self.assertEqual(str(self.car), "test_model")
