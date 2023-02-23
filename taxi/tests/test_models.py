from django.test import TestCase

from taxi.models import Driver, Manufacturer, Car


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.create(
            first_name="test_first_name",
            last_name="test_last_name",
            username="test_username",
            license_number="TST12345"
        )
        Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        Car.objects.create(
            model="test_model",
            manufacturer=Manufacturer.objects.get(name="test_name")
        )

    def test_driver_string_representation(self):
        driver = Driver.objects.get(username="test_username")
        self.assertEqual(
            str(driver),
            "test_username (test_first_name test_last_name)"
        )

    def test_get_absolut_url(self):
        driver = Driver.objects.get(username="test_username")
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")

    def test_manufacturer_string_representation(self):
        manufacturer = Manufacturer.objects.get(name="test_name")
        self.assertEqual(str(manufacturer), "test_name test_country")

    def test_car_string_representation(self):
        car = Car.objects.get(model="test_model")
        self.assertEqual(str(car), "test_model")
