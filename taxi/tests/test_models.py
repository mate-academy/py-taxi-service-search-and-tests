from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):

    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create(
            username="user1",
            first_name="first name",
            last_name="last name"
        )

    def test_model_manufacturer(self):
        self.assertEquals(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )

    def test_model_driver(self):

        self.assertEquals(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})"
        )

    def test_model_car(self):
        self.assertEquals(str(self.car), self.car.model)
