from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car
from django.contrib.auth import get_user_model


class ManufacturerModelTest(TestCase):
    def setUp(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_string_representation(self):
        manufacturer = Manufacturer.objects.get(name="Toyota")
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_ordering(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Audi", country="Germany")
        manufacturers = list(Manufacturer.objects.all())
        self.assertEqual(manufacturers[0].name, "Audi")
        self.assertEqual(manufacturers[1].name, "Ford")
        self.assertEqual(manufacturers[2].name, "Toyota")


class DriverModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="john",
            first_name="John",
            last_name="Doe",
            password="12345"
        )
        self.user.license_number = "123ABC"
        self.user.save()

    def test_string_representation(self):
        self.assertEqual(str(self.user), "john (John Doe)")

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            f"/drivers/{self.user.pk}/"
        )


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create_user(
            username="jane",
            first_name="Jane",
            last_name="Doe",
            password="54321"
        )
        self.car.drivers.add(self.driver)

    def test_string_representation(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_manufacturer_link(self):
        self.assertEqual(self.car.manufacturer, self.manufacturer)

    def test_driver_link(self):
        self.assertIn(self.driver, self.car.drivers.all())
