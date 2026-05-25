from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testdriver",
            password="12345",
            license_number="ABC12345"
        )
        self.client.login(username="testdriver", password="12345")

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_search_driver_by_username(self):
        response = self.client.get(reverse("taxi:driver-list"), {"q": "test"})
        self.assertContains(response, "testdriver")

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"q": "Corolla"})
        self.assertContains(response, "Corolla")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"q": "Toyota"}
        )
        self.assertContains(response, "Toyota")
