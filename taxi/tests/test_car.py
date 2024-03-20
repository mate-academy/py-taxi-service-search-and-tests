from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


CARS_ID = 1
CARS_LIST_URL = reverse("taxi:car-list")
CARS_DETAIL_URL = reverse("taxi:car-detail", args=[CARS_ID])


class PublicCarTests(TestCase):
    def test_login_required_list_page(self):
        resp = self.client.get(CARS_LIST_URL)

        self.assertNotEqual(resp.status_code, 200)

    def test_login_required_detail_page(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Ukraine"
        )
        Car.objects.create(
            id=CARS_ID,
            model="Test model",
            manufacturer=manufacturer,
        )
        resp = self.client.get(CARS_DETAIL_URL)

        self.assertNotEqual(resp.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="LIC12345",
        )

        self.client.force_login(self.user)

    def test_retrieve_list_page(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Ukraine"
        )
        Car.objects.create(
            model="Frist test model",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Second test model",
            manufacturer=manufacturer,
        )

        resp = self.client.get(CARS_LIST_URL)

        cars = Car.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["car_list"]),
            list(cars),
        )

    def test_retrieve_detail_page(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Ukraine"
        )
        Car.objects.create(
            id=CARS_ID,
            model="Frist test model",
            manufacturer=manufacturer,
        )

        resp = self.client.get(CARS_DETAIL_URL)

        self.assertEqual(resp.status_code, 200)

    def test_search_form_list_page(self):
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Ukraine"
        )
        Car.objects.create(
            model="Frist car",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="SECOND_CAR",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="Third",
            manufacturer=manufacturer,
        )

        searching_data = {"model": "car"}
        resp = self.client.get(CARS_LIST_URL, data=searching_data)

        cars = Car.objects.filter(model__icontains="car")

        self.assertEqual(
            list(resp.context["car_list"]),
            list(cars),
        )
