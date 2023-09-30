from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.models import Driver


class DriverTestCase(TestCase):
    def setUp(self):

        self.driver1 = Driver.objects.create(
            username="test1",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create(
            username="test2",
            first_name="Jane",
            last_name="Smith",
            license_number="XYZ67890"
        )

    def test_get_full_name(self):

        self.assertEqual(self.driver1.get_full_name(), "John Doe")
        self.assertEqual(self.driver2.get_full_name(), "Jane Smith")

        from taxi.models import Manufacturer, Car

        class ModelTests(TestCase):
            def test_manufacturer_str(self):
                manufacturer = Manufacturer.objects.create(
                    name="Toyota", country="Japan"
                )
                self.assertEquals(
                    str(manufacturer),
                    f"{manufacturer.name} "
                    f"{manufacturer.country}"
                )

            def test_car_str(self):
                car = Car.objects.create(
                    model="Model X",
                    manufacturer=Manufacturer.objects.create(
                        name="Tesla", country="USA"
                    ),
                )
                self.assertEquals(str(car), car.model)

            def test_driver_str(self):
                driver = get_user_model().objects.create(
                    username="johnsmith",
                    password="Qfd123***",
                    license_number="IGD43268",
                )
                self.assertEquals(
                    str(driver),
                    f"{driver.username} "
                    f"({driver.first_name} "
                    f"{driver.last_name})",
                )
