from django.urls import reverse
from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer1",
            country="Country1"
        )

        Car.objects.create(model="ModelA", manufacturer=manufacturer)
        Car.objects.create(model="ModelB", manufacturer=manufacturer)
        Car.objects.create(model="ModelС", manufacturer=manufacturer)

    def test_search_by_name(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=ModelA"
        )
        self.assertContains(response, "ModelA")
        self.assertNotContains(response, "ModelB")

    def test_search_empty(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=NonExistentCar"
        )
        self.assertContains(
            response, "There are no cars in taxi"
        )
