from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


class PublicCarTest(TestCase):
    def test_login_list_required(self):
        result_list = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(result_list.status_code, 200)

    def test_login_create_required(self):
        result_create = self.client.get(CAR_CREATE_URL)

        self.assertNotEqual(result_create.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            "test_name_username",
            "test_password"
        )
        self.client.force_login(self.driver)

        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

    def test_login_create_required(self):
        Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html")

    def test_login_update_required(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        url = reverse("taxi:car-update", args=[car.pk])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)

    def test_login_delete_required(self):
        car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        url = reverse("taxi:car-delete", args=[car.pk])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
