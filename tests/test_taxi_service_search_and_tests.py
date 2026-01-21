from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ManufacturerTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Tavria",
            country="Ukraine"
        )

    def test_model_creation(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(manufacturer.name, "Tesla")
        self.assertEqual(manufacturer.country, "USA")

    def test_str_method(self):
        manufacturer = Manufacturer.objects.get(id=1)
        self.assertEqual(str(manufacturer), "Tesla USA")

    def test_ordering(self):
        manufacturers = Manufacturer.objects.all().order_by("name")
        self.assertEqual(manufacturers[0].name, "Tavria")
        self.assertEqual(manufacturers[1].name, "Tesla")

    def test_uniques(self):
        with self.assertRaises(Exception):
            Manufacturer.objects.create(
                name="Tesla",
                country="USA"
            )

    def test_field_max_length(self):
        manufacturer = Manufacturer(name="A" * 300, country="German")
        with self.assertRaises(Exception):
            manufacturer.full_clean()

    def test_search(self):
        result = Manufacturer.objects.filter(name__icontains="Tes")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Tesla")


class DriverTest(TestCase):
    def setUp(self):
        self.driver1 = Driver.objects.create(
            username="driver1",
            password="123",
        )

    def test_str_method(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(str(driver), "driver1 ( )")

    def test_get_absolute_url(self):
        driver = Driver.objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")

    def test_search(self):
        result = Driver.objects.filter(username__icontains="dri")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].username, "driver1")


class CarTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(username="driver1", password="123")
        self.manufacturer = Manufacturer.objects.create(
            name="Mercedes",
            country="German"
        )
        self.car = Car.objects.create(
            model="300",
            manufacturer=self.manufacturer
        )
        self.car.drivers.set([self.driver])

    def test_str_method(self):
        self.assertEqual(str(self.car), "300")

    def test_search(self):
        result = Car.objects.filter(model__icontains="3")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].model, "300")
