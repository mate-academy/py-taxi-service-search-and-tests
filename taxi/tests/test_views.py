from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer

User = get_user_model()


class CustomViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )

        cls.driver1 = User.objects.create_user(
            username="jonathan.byers",
            password="pass123",
            license_number="JON12345",
        )
        cls.driver2 = User.objects.create_user(
            username="nancy.wheeler",
            password="pass123",
            license_number="NAN12345",
        )

        cls.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        cls.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )

        cls.car1 = Car.objects.create(
            model="Yaris",
            manufacturer=cls.manufacturer1,
        )
        cls.car2 = Car.objects.create(
            model="Focus",
            manufacturer=cls.manufacturer2,
        )

    def setUp(self):
        self.client = Client()
        self.client.login(
            username="testuser",
            password="testpass123",
        )

    def test_toggle_assign_to_car_add_and_remove(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car1.id])

        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car1.id]),
        )
        self.assertIn(self.user, self.car1.drivers.all())

        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car1.id]),
        )
        self.assertNotIn(self.user, self.car1.drivers.all())

    def test_driver_search_filtering(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"search": "jonathan"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "jonathan.byers")
        self.assertNotContains(response, "nancy.wheeler")

    def test_car_search_filtering(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"search": "Yaris"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Yaris")
        self.assertNotContains(response, "Focus")

    def test_manufacturer_search_filtering(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"search": "Toyota"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
