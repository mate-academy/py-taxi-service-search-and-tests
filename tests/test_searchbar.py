from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class SearchBarTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)

        self.toyota = Manufacturer.objects.create(name="Toyota",
                                                  country="Japan")
        self.honda = Manufacturer.objects.create(name="Honda",
                                                 country="Japan")

        Driver.objects.create(username="driver_a",
                              license_number="AAA12345")
        Driver.objects.create(username="driver_b",
                              license_number="BBB12345")

        Car.objects.create(model="Civic",
                           manufacturer=self.honda)
        Car.objects.create(model="Corolla",
                           manufacturer=self.toyota)

    def test_searchbar_for_manufacturer(self):
        reverse_test = reverse("taxi:manufacturer-list")
        response = self.client.get(reverse_test, {"title": "Toyota"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Honda")

    def test_searchbar_for_driver(self):
        reverse_test = reverse("taxi:driver-list")
        response = self.client.get(reverse_test, {"title": "driver_a"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver_a")
        self.assertNotContains(response, "driver_b")

    def test_searchbar_for_car(self):
        reverse_test = reverse("taxi:car-list")
        response = self.client.get(reverse_test, {"title": "Civic"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Civic")
        self.assertNotContains(response, "Corolla")
