from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer
from django.contrib.auth import get_user_model


class ManufacturerModelTest(TestCase):
    def test_manufacturer(self):
        obj = Manufacturer.objects.create(name="test", country="test_country")
        self.assertEqual(str(obj), f"{obj.name} {obj.country}")

    def test_manufacturer_ordering_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")

        names = list(Manufacturer.objects.values_list("name", flat=True))

        self.assertEqual(names, ["Audi", "BMW", "Toyota"])


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test12345",
            license_number="ABC12345",
        )

    def test_get_absolute_url(self):

        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
        )


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Model_test", country="Test_country"
        )
        self.car = Car.objects.create(
            model="BMW", manufacturer=self.manufacturer
        )

    def test_car_drivers_many_to_many(self):
        driver1 = get_user_model().objects.create_user(
            username="driver1", password="pass12345", license_number="AAA11111"
        )

        driver2 = get_user_model().objects.create_user(
            username="driver2", password="pass12345", license_number="BBB22222"
        )

        self.car.drivers.add(driver1, driver2)

        self.assertEqual(self.car.drivers.count(), 2)
        self.assertIn(driver1, self.car.drivers.all())
        self.assertIn(self.car, driver1.cars.all())
