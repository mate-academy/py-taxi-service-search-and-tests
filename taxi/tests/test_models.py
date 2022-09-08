from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMV",
            country="Germany"
        )

        self.assertEqual(str(manufacturer), "BMV Germany")

    def test_driver_str_and_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="m_shum",
            password="schumacher12345",
            first_name="Michael",
            last_name="Schumacher"
        )

        self.assertEqual(str(driver), "m_shum (Michael Schumacher)")
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMV",
            country="Germany"
        )
        car = Car.objects.create(
            model="X5",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)
