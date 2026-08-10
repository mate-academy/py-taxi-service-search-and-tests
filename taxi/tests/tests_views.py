from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class SearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="DL123456"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_driver_search(self):
        Driver.objects.create(username="JohnDoe")
        response = self.client.get(reverse(
            "taxi:driver-list") + "?username=John")
        self.assertContains(response, "JohnDoe")

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Ford", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:car-list") + "?model=Ford")
        self.assertContains(response, "Ford")

    def test_manufacture_search(self):
        Manufacturer.objects.create(name="Ford")
        response = (self.client.get
                    (reverse("taxi:manufacturer-list") + "?name=Ford"))
        self.assertContains(response, "Ford")
