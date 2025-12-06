from django.test import TestCase
from taxi.models import Car, Manufacturer, Driver


class CarSearchTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer_tesla = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        cls.manufacturer_toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        cls.driver_john = Driver.objects.create(
            username="John Doe",
            license_number="ABC123"
        )
        cls.driver_jane = Driver.objects.create(
            username="Jane Smith",
            license_number="XYZ789"
        )

        cls.car1 = Car.objects.create(
            model="Model S",
            manufacturer=cls.manufacturer_tesla
        )
        cls.car2 = Car.objects.create(
            model="Model 3",
            manufacturer=cls.manufacturer_tesla
        )
        cls.car3 = Car.objects.create(
            model="Corolla",
            manufacturer=cls.manufacturer_toyota
        )

        cls.car1.drivers.add(cls.driver_john)
        cls.car2.drivers.add(cls.driver_john, cls.driver_jane)
        cls.car3.drivers.add(cls.driver_jane)

    def test_search_car_by_model(self):
        results = Car.objects.filter(model__icontains="Model")
        self.assertEqual(len(results), 2)
        self.assertIn(self.car1, results)
        self.assertIn(self.car2, results)

    def test_search_car_by_manufacturer(self):
        results = Car.objects.filter(manufacturer__name__icontains="Tesla")
        self.assertEqual(len(results), 2)
        self.assertIn(self.car1, results)
        self.assertIn(self.car2, results)

    def test_search_car_by_driver(self):
        results = Car.objects.filter(drivers__username__icontains="John")
        self.assertEqual(len(results), 2)  # Джон управляет Model S и Model 3
        self.assertIn(self.car1, results)
        self.assertIn(self.car2, results)

        results = Car.objects.filter(drivers__username__icontains="Jane")
        self.assertEqual(len(results), 2)  # Джейн управляет Model 3 и Corolla
        self.assertIn(self.car2, results)
        self.assertIn(self.car3, results)

    def test_search_car_non_existing(self):
        results = Car.objects.filter(model__icontains="NonExistent")
        self.assertEqual(len(results), 0)
