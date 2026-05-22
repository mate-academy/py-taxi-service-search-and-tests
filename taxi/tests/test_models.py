from django import test
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class TestManufacturerModel(test.TestCase):
    def test_manufacturer_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        expected = "Toyota Japan"
        self.assertEqual(str(manufacturer), expected)


class TestDriverModel(test.TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            pk=10,
            username="johndoe",
            password="JohnDoe4",
            first_name="John",
            last_name="Doe",
        )

    def test_driver_str_method(self):
        expected = "johndoe (John Doe)"
        self.assertEqual(str(self.driver), expected)

    def test_driver_absolute_url(self):
        expected = reverse("taxi:driver-detail", kwargs={"pk": 10})
        self.assertEqual(self.driver.get_absolute_url(), expected)


class TestCarModel(test.TestCase):
    def test_car_str_method(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(model="Model X", manufacturer=manufacturer)
        expected = "Model X"
        self.assertEqual(str(car), expected)
