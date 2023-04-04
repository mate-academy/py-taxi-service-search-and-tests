from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer
from django.contrib.auth import get_user_model


class ToggleAssignToCarTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver = get_user_model().objects.create(
            username="testuser", password="testpass", license_number="12345"
        )
        self.manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        self.car = Car.objects.create(
            manufacturer=self.manufacturer,
            model="Test Model",
        )

    def test_toggle_assign_to_car(self):
        self.client.force_login(self.driver)
        response = self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:car-detail", args=[self.car.id]))
        self.driver.refresh_from_db()
        if self.car in self.driver.cars.all():
            self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
            self.assertNotIn(self.car, self.driver.cars.all())
        else:
            self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
            self.assertIn(self.car, self.driver.cars.all())
