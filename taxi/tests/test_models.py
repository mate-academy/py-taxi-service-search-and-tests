from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


# Create your tests here.
class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        self.assertEquals(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(username="test", first_name="test_first", last_name="test_second")
        self.assertEquals(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        car =  Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEquals(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test"
        license_number = "test_num"
        password = "test1234"
        driver = get_user_model().objects.create_user(username=username, license_number=license_number, password=password)
        self.assertEquals(driver.username, username)
        self.assertEquals(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

