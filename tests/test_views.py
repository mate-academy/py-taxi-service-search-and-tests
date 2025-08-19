from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test",
            password="test123",
            license_number="TES99999"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Maserati", country="Italy"
        )
        self.car = Car.objects.create(
            model="GranTurismo", manufacturer=self.manufacturer
        )
        self.client.login(username="test", password="test123")

    def test_toggle_assign_adds_car(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertIn(self.car, self.driver.cars.all())
        self.assertRedirects(
            response,
            reverse(
                "taxi:car-detail",
                args=[self.car.id]
            )
        )

    def test_toggle_assign_removes_car(self):
        self.driver.cars.add(self.car)
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )
        self.assertNotIn(self.car, self.driver.cars.all())
        self.assertRedirects(
            response,
            reverse(
                "taxi:car-detail",
                args=[self.car.id]
            )
        )

    def test_toggle_assign_multiple_times(self):
        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.assertIn(self.car, self.driver.cars.all())

        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.assertNotIn(self.car, self.driver.cars.all())

        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))
        self.assertIn(self.car, self.driver.cars.all())
