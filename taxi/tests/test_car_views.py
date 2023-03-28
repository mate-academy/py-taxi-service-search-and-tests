from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CARS_URL = reverse("taxi:car-list")


class PublicCarsTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CARS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarsTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="testuser", password="test123user"
        )
        self.client.force_login(self.driver)

        manufacturer1 = Manufacturer.objects.create(
            name="Manufacturer Name 1",
            country="Manufacturer Country 1"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Manufacturer Name 2",
            country="Manufacturer Country 2"
        )

        self.car1 = Car.objects.create(
            model="Car1", manufacturer=manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Car2", manufacturer=manufacturer2
        )

    def test_retrieve_cars(self):
        cars = Car.objects.all()

        response = self.client.get(CARS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_listed(self):
        response = self.client.get(CARS_URL)

        for element in [
            self.car1.id,
            self.car1.model,
            self.car1.manufacturer.name,
            self.car2.id,
            self.car2.model,
            self.car2.manufacturer.name,
        ]:
            self.assertContains(response, element)

    def test_search_car(self):
        response = self.client.get(CARS_URL + "?search_by=ar1")

        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car1.manufacturer.name)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car2.manufacturer.name)

        response = self.client.get(CARS_URL + "?search_by=a")

        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car1.manufacturer.name)
        self.assertContains(response, self.car2.model)
        self.assertContains(response, self.car2.manufacturer.name)

        response = self.client.get(CARS_URL + "?search_by=super")

        self.assertNotContains(response, self.car1.model)
        self.assertNotContains(response, self.car1.manufacturer.name)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car2.manufacturer.name)
