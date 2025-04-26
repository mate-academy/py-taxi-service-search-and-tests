from django.urls import reverse
from django.test import TestCase
from taxi.models import Driver, Car, Manufacturer
from django.contrib.auth import get_user_model


class SearchFunctionalityTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="adminpass123",
            is_staff=True
        )
        self.client.login(username="admin", password="adminpass123")

        self.manufacturer = Manufacturer.objects.create(
            name="Ford", country="USA"
        )
        self.car = Car.objects.create(
            model="BMW", manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create_user(
            username="testuser1",
            password="testpass123",
            license_number="ABC12345"
        )

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=testuser1"
        )
        self.assertContains(response, "testuser1")

    def test_car_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=BMW")
        self.assertContains(response, "BMW")

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Ford"
        )
        self.assertContains(response, "Ford")
