from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car
CAR_LIST_URL = reverse("taxi:car-list")


class PrivateCar(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_search_car(self):
        manufacturer = Manufacturer.objects.create(name="name_two",
                                                   country="country_two")
        Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="test_two",
            manufacturer=manufacturer
        )
        search_data = {"model": "test"}
        resp = self.client.get(CAR_LIST_URL, data=search_data)
        car = Car.objects.filter(model__icontains="test")

        self.assertEqual(
            list(resp.context["car_list"]),
            list(car)
        )
