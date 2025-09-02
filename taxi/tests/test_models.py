from django.test import TestCase
from django.urls import reverse


from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test country"
        )
        self.assertEqual(str(manufacturer), f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test",
            password="1234",
            license_number="tes1234"
        )

        self.assertEqual(str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})")

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create(
            username="test",
            password="1234",
            license_number="tes1234"
        )
        self.assertEqual(driver.get_absolute_url(), reverse("taxi:driver-detail", kwargs={"pk": driver.pk}))

    def test_car_str(self):
        driver = Driver.objects.create(
            username="test",
            password="1234",
            license_number="tes1234"
        )
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test country"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), car.model)

