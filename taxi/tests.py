from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car, Driver


class ListViewSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model.objects.create_user(
            username="testUser", password="<PASSWORD>"
        )
        self.client.force_login(self.user)

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="BMW", country="US")
        Manufacturer.objects.create(name="Toyota", country="Germany")

        res = self.client.get(reverse("taxi:manufacturer-list"), {"name": "Toyota"})
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "BMW")


    def test_car_search(self):
        m = Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(model="X5", manufacturer=m)
        Car.objects.create(model="Focus", manufacturer=m)

        res = self.client.get(reverse("taxi:car-list"), {"Model": "X5"})
        self.assertContains(res, "X5")
        self.assertNotContains(res, "Focus")

    def test_driver_search(self):
        Driver.objects.create_user(username="john_doe", password="1234", license_number="ABC12345")
        Driver.objects.create_user(username="jane_smith", password="1234", license_number="XYZ67890")

        res = self.client.get(reverse("taxi:driver-list"), {"username": "john"})
        self.assertContains(res, "john_doe")
        self.assertNotContains(res, "jane_smith")
