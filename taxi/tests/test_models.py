from django.test import TestCase

from taxi.models import Manufacturer, Driver, Car


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create_user(
            username="test",
            first_name="test1",
            last_name="test2",
            password="test"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="name",
            country="country"
        )
        self.car = Car.objects.create(model="model", manufacturer=self.manufacturer)

    def test_str_method(self):
        self.assertEqual(str(self.manufacturer), "name country")
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} ({self.driver.first_name} {self.driver.last_name})"
        )
        self.assertEqual(str(self.car), self.car.model)

    def test_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            f"/drivers/{self.driver.pk}/"
        )


