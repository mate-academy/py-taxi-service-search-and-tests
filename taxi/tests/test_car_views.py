from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from taxi.models import Manufacturer, Car

CARS_ID = 1
CARS_LIST_URL = reverse("taxi:car-list")
CARS_DETAIL_URL = reverse("taxi:car-detail", args=[CARS_ID])


class PublicCarViewsTests(TestCase):
    def test_login_required_car_list_page(self):
        resp = self.client.get(CARS_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_car_detail_page(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer1",
            country="USA"
        )
        Car.objects.create(
            id=CARS_ID,
            model="Car1",
            manufacturer=manufacturer,
        )
        resp = self.client.get(CARS_DETAIL_URL)

        self.assertNotEqual(resp.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="TEST",
            password="Test1234!",
            license_number="ABC12345",
        )

        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer1",
            country="USA"
        )

        self.car1 = Car.objects.create(
            id=CARS_ID,
            model="Car1",
            manufacturer=self.manufacturer,
        )
        self.car2 = Car.objects.create(
            model="Car2",
            manufacturer=self.manufacturer,
        )

    def test_get_car_list_page(self):
        resp = self.client.get(CARS_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["car_list"]),
            list(cars),
        )

    def test_get_car_detail_page(self):
        resp = self.client.get(CARS_DETAIL_URL)
        model = resp.context["car"].model

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(model, self.car1.model)
