from django.test import TestCase

from taxi.models import Car, Manufacturer, Driver


class CarModelTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="3 Series",
            manufacturer=manufacturer
        )

    def test_model_label(self):
        field_label = self.car._meta.get_field("model").verbose_name
        self.assertEqual(field_label, "model")

    def test_model_max_length(self):
        max_length = self.car._meta.get_field("model").max_length
        self.assertEqual(max_length, 255)

    def test_manufacturer_label(self):
        field_label = self.car._meta.get_field("manufacturer").verbose_name
        self.assertEqual(field_label, "manufacturer")

    def test_drivers_label(self):
        field_label = self.car._meta.get_field("drivers").verbose_name
        self.assertEqual(field_label, "drivers")

    def test_car_str(self):
        expected = self.car.model
        self.assertEqual(expected, str(self.car))

    def test_drivers_related_name(self):
        driver = Driver.objects.create_user(
            username="Test",
            password="1234",
            license_number="ABC12345"
        )
        self.car.drivers.add(driver)
        self.assertTrue(driver.cars.all())
