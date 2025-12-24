from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Driver, Car, Manufacturer


# Create your tests here.


class SearchTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        self.driver1 = Driver.objects.create(
            username="driver1", license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create(
            username="driver2", license_number="DEF67890"
        )
        self.car1 = Car.objects.create(
            model="ModelX",
            manufacturer=Manufacturer.objects.create(
                name="Tesla",
                country="USA"
            ),
        )
        self.car2 = Car.objects.create(
            model="M3",
            manufacturer=Manufacturer.objects.create(
                name="BMW",
                country="Germany"
            ),
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_search_drivers(self):
        response = self.client.get(reverse("taxi:driver-list") + "?q=driver1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    def test_search_cars(self):
        response = self.client.get(reverse("taxi:car-list") + "?q=ModelX")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ModelX")
        self.assertNotContains(response, "M3")

    def test_search_manufacturers(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?q=Toyota"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
