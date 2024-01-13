from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=Manufacturer.objects.create(
                name="TestManufacturer"
            )
        )

    def test_index_view_with_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:index"))
        drivers = response.context[0]["num_drivers"]
        cars = response.context[0]["num_cars"]
        manufacturers = response.context[0]["num_manufacturers"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(drivers, Driver.objects.count())
        self.assertEqual(cars, Car.objects.count())
        self.assertEqual(manufacturers, Manufacturer.objects.count())

    def test_index_view_without_login(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("taxi:index")
        )
