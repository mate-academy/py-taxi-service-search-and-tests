from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsTest(TestCase):
    def test_manufacture(self):
        obj1 = Manufacturer.objects.create(
            name="Hello",
            country="Hello2",
        )

        self.assertEqual(str(obj1), f"{obj1.name} {obj1.country}")

    def test_driver(self):
        obj1 = Driver.objects.create(
            license_number="HFN22222",
            username="admin",
            first_name="admin",
            last_name="admin",
        )

        self.assertEqual(str(obj1),
                         f"{obj1.username} ({obj1.first_name} "
                         f"{obj1.last_name})",
                         )
        self.assertEqual(obj1.get_absolute_url(),
                         f"/drivers/{obj1.id}/")

    def test_car(self):
        manufacturer = Manufacturer.objects.create(
            name="h1",
            country="h2",
        )

        driver = Driver.objects.create(
            username="h1",
            password="123123",
        )

        obj1 = Car.objects.create(
            model="h3",
            manufacturer=manufacturer,
        )
        obj1.drivers.add(driver)
        obj1.save()
        self.assertEqual(str(obj1), obj1.model)
