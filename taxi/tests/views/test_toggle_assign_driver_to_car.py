from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from taxi.models import Car, Manufacturer


class MyTestCase(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="usertest",
            password="testpassword456",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United Kingdom",
        )
        self.car = Car.objects.create(
            model="Test Car", manufacturer_id=self.manufacturer.id
        )
        self.client.force_login(self.driver)

    def test_toggle_assign_driver_to_car_login_required(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy("taxi:toggle-car-assign", args=[self.car.pk])
        )

        self.assertNotEqual(response.status_code, 200)

    def test_toggle_assign_driver_to_car_view(self):
        self.assertFalse(self.car in self.driver.cars.all())

        response = self.client.get(
            reverse_lazy("taxi:toggle-car-assign", args=[self.car.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.driver in self.car.drivers.all())

        response = self.client.get(
            reverse_lazy("taxi:toggle-car-assign", args=[self.car.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.driver in self.car.drivers.all())
