from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_car_list(self) -> None:
        result = self.client.get(CAR_LIST_URL)

        self.assertNotEquals(result.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer_obj = Manufacturer.objects.create(
            name="test1",
            country="country1"
        )

    def test_car_list(self) -> None:
        Car.objects.create(
            model="test1",
            manufacturer=self.manufacturer_obj
        )
        Car.objects.create(
            model="test2",
            manufacturer=self.manufacturer_obj
        )

        result = self.client.get(CAR_LIST_URL)

        self.assertEquals(result.status_code, 200)
        self.assertEquals(
            list(result.context["car_list"]),
            list(Car.objects.all())
        )
