from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

class ManufacturerTests(TestCase):
    def test_default_ordering(self):
        Manufacturer.objects.bulk_create([
            Manufacturer(name="A", country="-"),
            Manufacturer(name="B", country="-"),
            Manufacturer(name="CC", country="-"),
            Manufacturer(name="DDDDD", country="-"),
            Manufacturer(name="zzzZZ", country="-"),
            Manufacturer(name="name", country="-"),
            Manufacturer(name="4agagagsdfs", country="-"),
        ])

        self.assertEqual(
            list(Manufacturer.objects.all()),
            list(Manufacturer.objects.all().order_by("name"))
        )

    def test_str(self):
        name = "test_name",
        country = "test_country"

        manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )

        self.assertEqual(str(manufacturer), f"{name} {country}")


class DriverTests(TestCase):
    def test_str(self):
        username = "test_username"
        first_name = "test_first_name"
        last_name = "test_last_name"

        driver = Driver.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            license_number="test_license_number"
        )

        self.assertEqual(str(driver), f"{username} ({first_name} {last_name})")

    def test_get_absolute_url(self):
        driver = Driver.objects.create_user(
            username="test_username",
            license_number="test_license_number"
        )
        self.assertEqual(driver.get_absolute_url(), reverse("taxi:driver-detail", kwargs={"pk": driver.pk}))


class CarTests(TestCase):
    def test_str(self):
        model = "test_model"
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        
        car = Car.objects.create(
            model=model,
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), model)