from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelsStrTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer_obj = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.driver_obj = Driver.objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name"
        )

    def test_manufacturer(self) -> None:
        self.assertEquals(str(self.manufacturer_obj), "test_name test_country")

    def test_driver(self) -> None:
        self.assertEquals(
            str(self.driver_obj),
            f"{self.driver_obj.username} "
            f"({self.driver_obj.first_name} {self.driver_obj.last_name})"
        )

    def test_car(self) -> None:
        obj = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer_obj
        )
        self.assertEquals(str(obj), "test_model")
