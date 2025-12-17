from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Driver, Car

User = get_user_model()


class ModelsTestCase(TestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan"
                                                        )
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="password123",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer
                                      )
        self.car.drivers.add(self.driver)

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer),
                         "Toyota Japan"
                         )

    def test_driver_str(self):
        self.assertEqual(str(self.driver),
                         "driver1 (John Doe)"
                         )

    def test_driver_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        self.assertIn(str(self.driver.pk), url)
        self.assertTrue(url.startswith("/"))

    def test_car_str(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_car_has_driver(self):
        self.assertIn(self.driver, self.car.drivers.all())

    def test_driver_has_car(self):
        self.assertIn(self.car, self.driver.cars.all())

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="Audi", country="Germany")
        manufacturers = list(Manufacturer.objects.all())
        self.assertEqual(manufacturers[0].name, "Audi")
        self.assertEqual(manufacturers[1].name, "Toyota")
