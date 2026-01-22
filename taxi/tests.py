
from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        """Set up test data for the test case."""
        self.driver1 = Driver.objects.create_user(
            username="driver1",
            password="testpass",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="testpass",
            first_name="Jane",
            last_name="Smith",
            license_number="DEF12345"
        )

        self.manufacturer = Manufacturer.objects.create(name="Tesla",
                                                        country="USA")
        self.car = Car.objects.create(model="Model S",
                                      manufacturer=self.manufacturer)

        self.client.login(username="driver1", password="testpass")

    def test_driver_search(self):
        """Test searching for a driver by username."""
        response = self.client.get(reverse("taxi:driver-list") + "?q=driver1")
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)

    def test_car_search(self):
        """Test searching for a car by model."""
        response = self.client.get(reverse("taxi:car-list") + "?q=Model S")
        self.assertContains(response, self.car.model)

    def test_manufacturer_search(self):
        """Test searching for a manufacturer by name."""
        response = self.client.get(reverse(
            "taxi:manufacturer-list") + "?q=Tesla")
        print(response.content.decode())
        self.assertContains(response, "Tesla")
