from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer


class SearchFeatureTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testAdmin",
            password="password1234",
        )
        self.client.force_login(self.user)
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.driver1 = Driver.objects.create_user(
            username="bob.driver",
            license_number="AAA11111"
        )
        self.driver2 = Driver.objects.create_user(
            username="alice.smith",
            license_number="BBB22222"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Fiesta",
            manufacturer=self.manufacturer2
        )

    def test_manufacturer_search_by_name(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "Toy"})
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_car_search_by_model(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Cor"})
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Fiesta")

    def test_driver_search_by_username(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "alice"})
        self.assertContains(response, "alice.smith")
        self.assertNotContains(response, "bob.driver")

    def test_search_no_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "NonExistentCar"})
        self.assertEqual(len(response.context["car_list"]), 0)
