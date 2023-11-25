from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


# Create your tests here.
class DriverModelTest(TestCase):

    def setUp(self):
        self.driver = Driver.objects.create(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            license_number="ABC123"
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.username, "john_doe")
        self.assertEqual(self.driver.first_name, "John")
        self.assertEqual(self.driver.last_name, "Doe")
        self.assertEqual(self.driver.license_number, "ABC123")

    def test_str_representation(self):
        expected_str = "john_doe (John Doe)"
        self.assertEqual(str(self.driver), expected_str)

    def test_get_absolute_url(self):
        expected_url = reverse("taxi:driver-detail",
                               kwargs={"pk": self.driver.pk}
                               )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)


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


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="MAN INC", country="Germany")

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(id=1)
        expected_object_name = f"{manufacturer.name} {manufacturer.country}"
        self.assertEquals(str(manufacturer), expected_object_name)
