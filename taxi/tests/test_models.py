from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class TestReturnedStr(TestCase):

    @classmethod
    def setUpTestData(cls):
        _dr = get_user_model().objects.create_user(
            username="test-user",
        )
        _mf = Manufacturer.objects.create(
            name="test-manufacturer",
            country="test-country",
        )
        Car.objects.create(
            model="test-model",
            manufacturer=_mf,
        ).drivers.add(_dr)

    def test_driver_str(self):
        driver = get_user_model().objects.get(pk=1)

        self.assertEqual(
            driver.__str__(),
            driver.username,
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.get(pk=1)

        self.assertEqual(
            manufacturer.__str__(),
            f"{manufacturer.name} {manufacturer.country}",
        )

    def test_car_str(self):
        car = Car.objects.get(pk=1)

        self.assertEqual(car.__str__(), car.model)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(pk=1)

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )
