from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            license_number="JHG12345",
            password="pass12345word",
        )

        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Test", country="Test"
        )
        Car.objects.create(model="Car1", manufacturer=self.manufacturer)
        Car.objects.create(model="Car2q", manufacturer=self.manufacturer)
        Car.objects.create(model="Car3q", manufacturer=self.manufacturer)
        Car.objects.create(model="Car4", manufacturer=self.manufacturer)

    def test_retrieve_car(self):
        res = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["car_list"]), list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_search_car_by_model(self):
        res = self.client.get(CAR_LIST_URL + "?model=q")

        cars = Car.objects.filter(model__icontains="q")
        self.assertEqual(list(res.context["car_list"]), list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")
