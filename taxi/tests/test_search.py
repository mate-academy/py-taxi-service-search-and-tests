from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver


class PublicTaxiSearchTests(TestCase):
    def test_manufacturer_list_search(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_car_list_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="X5", manufacturer=manufacturer)

        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Corolla"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "X5")

    def test_driver_list_search(self):
        Driver.objects.create_user(username="johndoe", password="password123")
        Driver.objects.create_user(username="janedoe", password="password123")

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "johndoe"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "johndoe")
        self.assertNotContains(response, "janedoe")
