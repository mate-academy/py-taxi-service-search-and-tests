from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )
        self.driver = get_user_model().objects.create(
            username="test",
            first_name="test",
            last_name="test"
        )
        self.car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_login_required_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create(self):
        res = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_update(self):
        url = reverse("taxi:car-update", args=[self.car.id])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_delete(self):
        url = reverse("taxi:car-delete", args=[self.car.id])
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test"
        )

        self.client.force_login(self.driver)

    def test_retrieve_car_list(self):
        car = Car.objects.create(
            model="test",
            manufacturer=self.manufacturer
        )
        car.drivers.add(self.driver)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]),
                         list(cars))
        self.assertTemplateUsed(response,
                                "taxi/car_list.html")
