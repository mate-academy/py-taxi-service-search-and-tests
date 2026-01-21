from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class SearchTests(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(name="Ford", country="USA")

        self.car1 = Car.objects.create(model="Corolla", manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="Focus", manufacturer=self.manufacturer2)

        self.driver1 = get_user_model().objects.create_user(
            username="driver1", password="12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="john", password="12345"
        )

        self.driver1.cars.add(self.car1)
        self.driver2.cars.add(self.car2)

        self.client.force_login(self.driver1)  # логін для доступу до ListView

    def test_manufacturer_search(self):
        response = self.client.get(reverse("taxi:manufacturer-list") + "?name=Toyota")
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")


    # Car search
    def test_car_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Corolla")
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")


    # Driver search
    def test_driver_search(self):
        response = self.client.get(reverse("taxi:driver-list") + "?username=john")
        self.assertContains(response, "john")
        self.assertNotContains(response, "driver1")