from django.test import TestCase

from taxi.models import Driver, Car, Manufacturer


class ModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testusername",
            password="test1234",
            first_name="testfirst",
            last_name="testlast"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="testname",
            country="testcountry"
        )
        self.car = Car.objects.create(
            model="testmodel",
            manufacturer=self.manufacturer
        )

    def test_string_representation_of_driver(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})"
        )

    def test_string_representation_of_car(self):
        self.assertEqual(
            str(self.car),
            self.car.model
        )

    def test_string_representation_of_manufacturer(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_get_absolute_url_of_driver(self):
        self.assertEqual(self.driver.get_absolute_url(), "/drivers/1/")
