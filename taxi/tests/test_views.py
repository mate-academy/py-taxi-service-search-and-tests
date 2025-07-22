from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver
from django.contrib.auth import get_user_model


class ListViewSearchTests(TestCase):
    def setUp(self):
        # Створимо користувача для входу
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

        # Дані для тестів
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer2
        )

        self.driver1 = Driver.objects.create(
            username="driver_one", password="pass", license_number="ABC123"
        )

        self.driver2 = Driver.objects.create(
            username="anotherdriver", password="pass", license_number="XYZ789"
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=toy"
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Corolla"
        )
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

    def test_search_driver_by_username(self):
        response = self.client.get(reverse(
            "taxi:driver-list") + "?username=driver_one"
        )

        self.assertContains(response, "driver_one")
        self.assertNotContains(response, "anotherdriver")
