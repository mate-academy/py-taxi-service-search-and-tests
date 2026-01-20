from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class TaxiTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford", country="USA"
        )

        self.car1 = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Mustang", manufacturer=self.manufacturer2
        )

        self.driver1 = Driver.objects.create_user(
            username="test_driver_1",
            first_name="John",
            last_name="Doe",
            password="driverpassword",
            license_number="ABCD-12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="another_driver_2",
            first_name="Jane",
            last_name="Smith",
            password="driverpassword",
            license_number="EFGH-67890"
        )

    def test_search_drivers_by_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list") + "?q=test_driver")

        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)

    def test_search_cars_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?q=Corolla")

        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)

    def test_search_manufacturers_by_name(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list") + "?q=Toyota")

        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
