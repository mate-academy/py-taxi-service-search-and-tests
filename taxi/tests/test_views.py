from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicCarTest(TestCase):

    def test_login_required(self):
        res_list = self.client.get(CAR_LIST_URL)
        self.assertNotEquals(res_list.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(name="Test")
        self.car = Car.objects.create(model="Test 1", manufacturer=self.manufacturer)
        Car.objects.create(model="Test 2", manufacturer=self.manufacturer)
        self.CAR_DETAIL_URL = reverse("taxi:car-detail", args=[self.car.id])

    def test_retrieve_cars(self):
        res_list = self.client.get(CAR_LIST_URL)
        self.assertEqual(res_list.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(res_list.context["car_list"]), list(cars))
        self.assertTemplateUsed(res_list, "taxi/car_list.html")

    def test_retrieve_car(self):
        res_detail = self.client.get(self.CAR_DETAIL_URL)
        self.assertEqual(res_detail.status_code, 200)
        self.assertEqual(res_detail.context["car"], self.car)
        self.assertTemplateUsed(res_detail, "taxi/car_detail.html")

