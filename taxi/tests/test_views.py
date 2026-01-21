from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="pass12345",
            license_number="ABV12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        self.car = Car.objects.create(
            model="A7", manufacturer=self.manufacturer
        )
        self.client.login(username="testdriver", password="pass12345")

    def test_toggle_assign_adds_car(self):
        response = self.client.get(reverse(
            "taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertIn(self.car, self.driver.cars.all())
        self.assertEqual(response.status_code, 302)

    def test_toggle_assign_removes_car(self):
        self.driver.cars.add(self.car)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertNotIn(self.car, self.driver.cars.all())
        self.assertEqual(response.status_code, 302)
