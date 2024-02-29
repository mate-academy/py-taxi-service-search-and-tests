from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(
            name="SanchezInc.",
            country="Peperoni"
        )

    def test_manufacturer_str_method(self):
        manufacturer = Manufacturer.objects.get(name="SanchezInc.")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )


class DriverModelTest(TestCase):
    def setUp(self):
        Driver.objects.create(
            username="sanDiesel",
            first_name="Sanchez",
            last_name="Chebukez",
            license_number="MAN77777"
        )

    def test_driver_str_method(self):
        driver = Driver.objects.get(username="sanDiesel")
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_licence_number_exists(self):
        driver = Driver.objects.get(username="sanDiesel")
        self.assertEqual(driver.license_number, "MAN77777")

    def test_get_absolute_url_method(self):
        driver = Driver.objects.get(username="sanDiesel")
        url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), url)


class CarModelTest(TestCase):
    def setUp(self):
        Car.objects.create(
            model="Hurricane",
            manufacturer=Manufacturer.objects.create(
                name="SanchezInc.",
                country="Peperoni"
            )
        )

    def test_car_str_method(self):
        car = Car.objects.get(model="Hurricane")
        self.assertEqual(
            str(car), car.model
        )
