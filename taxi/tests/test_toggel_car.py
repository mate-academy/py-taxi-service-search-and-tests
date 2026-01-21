from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test user",
            license_number="LKA02485",
            password="<PASSWORD>",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Fiat",
            country="France"
        )
        self.car = Car.objects.create(
            model="Doblo",
            manufacturer=self.manufacturer,
        )
        self.client.force_login(self.driver)

    def test_assign_car_to_driver(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        response = self.client.post(url)
        self.assertIn(self.car, self.driver.cars.all())
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.car, self.driver.cars.all())

    def test_delete_car_from_driver(self):
        self.driver.cars.add(self.car)
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        self.assertIn(self.car, self.driver.cars.all())
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.car, self.driver.cars.all())
