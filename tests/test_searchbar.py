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
        responce = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"title": "Toyota"})

        self.assertEqual(responce.status_code, 200)
        self.assertContains(responce, "Toyota")
        self.assertNotContains(responce, "Honda")

    def test_searchbar_for_driver(self):
        responce = self.client.get(reverse("taxi:driver-list"),
                                   {"title": "driver_a"})

        self.assertEqual(responce.status_code, 200)
        self.assertContains(responce, "driver_a")
        self.assertNotContains(responce, "driver_b")

    def test_searchbar_for_car(self):
        responce = self.client.get(reverse("taxi:car-list"),
                                   {"title": "Civic"})

        self.assertEqual(responce.status_code, 200)
        self.assertContains(responce, "Civic")
        self.assertNotContains(responce, "Corolla")
