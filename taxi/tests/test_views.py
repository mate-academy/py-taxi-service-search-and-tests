from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer


class CustomViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="testpass123",
            license_number="XYZ99999"
        )
        self.client.login(
            username="user1",
            password="testpass123"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Mazda",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="CX-5",
            manufacturer=self.manufacturer
        )

    def test_index_view_context(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)

    def test_toggle_assign_adds_car_to_driver(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.car, self.user.cars.all())

    def test_toggle_assign_removes_car_from_driver(self):
        self.user.cars.add(self.car)
        url = reverse("taxi:toggle-car-assign", args=[self.car.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.car, self.user.cars.all())
