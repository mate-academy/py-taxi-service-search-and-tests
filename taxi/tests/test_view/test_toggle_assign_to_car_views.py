from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class AssignToCar(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="test_model",
        )

        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_assign_to_car(self):
        url_car = reverse("taxi:toggle-car-assign", args=[self.car.id])

        self.client.get(url_car)

        self.assertTrue(self.user in self.car.drivers.all())

    def test_cancel_assign_of_car(self):
        self.car.drivers.add(self.user)
        url_car = reverse("taxi:toggle-car-assign", args=[self.car.id])
        self.client.get(url_car)

        self.assertFalse(self.user in self.car.drivers.all())
