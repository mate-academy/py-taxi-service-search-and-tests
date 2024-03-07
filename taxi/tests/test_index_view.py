from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicTests(TestCase):
    def test_login_required_for_index_view_when_not_logged_in(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            first_name="Test",
            last_name="TesT",
            password="test123456",
            license_number="QWE12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.car = Car.objects.create(
            model="Cybertruck",
            manufacturer=self.manufacturer
        )
        self.client.force_login(self.user)

    def test_login_required_for_index_view_when_logged_in(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_manufacturers_are_counting_correctly(self):
        Manufacturer.objects.create(
            name="Tesla1",
            country="USA"
        )
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_manufacturers"], 2)

    def test_cars_are_counting_correctly(self):
        Car.objects.create(
            model="Cybertruck1",
            manufacturer=self.manufacturer
        )
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_cars"], 2)

    def test_drivers_are_counting_correctly(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_drivers"], 1)

    def test_visits_counter(self):
        for _ in range(100):
            response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.context["num_visits"], 100)
