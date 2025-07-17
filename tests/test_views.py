from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        # Manufacturers
        self.manufacturer1 = (
            Manufacturer.objects.create(name="Tesla",
                                        country="USA"))
        self.manufacturer2 = (
            Manufacturer.objects.create(name="Toyota",
                                        country="Japan"))

        # Cars
        self.car1 = Car.objects.create(model="Tesla X",
                                       manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="Corolla",
                                       manufacturer=self.manufacturer2)

        # Drivers
        self.driver1 = Driver.objects.create_user(
            username="johnny", password="pass",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="sarah", password="pass",
            license_number="XYZ67890"
        )

        # ✅ Login
        self.client.login(username="johnny", password="pass")

    def test_driver_search(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "john"})
        self.assertContains(response, "johnny")
        self.assertNotContains(response, "sarah")

    def test_car_search(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "Tes"})
        self.assertContains(response, "Tesla X")
        self.assertNotContains(response, "Corolla")

    def test_manufacturer_search(self):
        response = \
            (self.client.get(reverse("taxi:manufacturer-list"),
                             {"name": "Toyota"}))
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Tesla")
