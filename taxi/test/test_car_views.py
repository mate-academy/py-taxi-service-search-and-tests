from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car1 = Car.objects.create(
            model="test1_model",
            manufacturer=self.manufacturer,
        )
        self.car1.drivers.set((self.user,))

    def test_retrieve_car(self):
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(
            res,
            "taxi/car_list.html"
        )

    def test_search_cars(self):
        res = self.client.get(CAR_URL + "?model=1")
        car = Car.objects.filter(model__icontains="1")
        self.assertEqual(
            list(res.context["car_list"]),
            list(car)
        )

    def test_create_car(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "new_car",
                "drivers": [self.user.id],
                "manufacturer": self.manufacturer.id
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Car.objects.filter(model="new_car").exists()
        )
