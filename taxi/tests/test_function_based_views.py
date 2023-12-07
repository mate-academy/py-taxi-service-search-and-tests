from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


INDEX_URL = reverse("taxi:index")


def toggle_assign_url(pk: int) -> str:
    return reverse("taxi:toggle-car-assign", args=[pk])


class PrivateManufacturerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Africa",
        )

        cls.car = Car.objects.create(
            model="Test Car",
            manufacturer=manufacturer,
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_index(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        num_drivers = Driver.objects.count()
        num_cars = Car.objects.count()
        num_manufacturers = Manufacturer.objects.count()
        self.assertEqual(response.context["num_drivers"], num_drivers)
        self.assertEqual(response.context["num_cars"], num_cars)
        self.assertEqual(
            response.context["num_manufacturers"],
            num_manufacturers,
        )
        self.assertEqual(response.context["num_visits"], 1)

    def test_toggle_assign_to_car(self):
        response = self.client.get(toggle_assign_url(1))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.cars.filter(pk=1).exists())

        response = self.client.get(toggle_assign_url(1))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user.cars.filter(pk=1).exists())
