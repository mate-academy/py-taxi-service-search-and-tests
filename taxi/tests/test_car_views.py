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
            username="testuser",
            password="test123user"
        )
        self.client.force_login(self.driver)

        manuf1 = Manufacturer.objects.create(
            name="Manufname1",
            country="Manufcountry1"
        )
        manuf2 = Manufacturer.objects.create(
            name="Manufname2",
            country="Manufcountry2"
        )

        self.car1 = Car.objects.create(
            model="Car1",
            manufacturer=manuf1
        )
        self.car2 = Car.objects.create(
            model="Car2",
            manufacturer=manuf2
        )

    def test_retrieve_cars(self):
        cars = Car.objects.all()

        response = self.client.get(CARS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_listed(self):
        response = self.client.get(CARS_URL)

        self.assertContains(response, self.car1.id)
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car1.manufacturer)
        self.assertContains(response, self.car2.id)
        self.assertContains(response, self.car2.model)
        self.assertContains(response, self.car2.manufacturer)
