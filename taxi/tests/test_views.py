from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_listlview(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="11111",
        )
        self.client.force_login(self.user)

    def test_login_retrive_user(self):
        man = Manufacturer.objects.create(name="Manufacturer1")
        Car.objects.create(model="TT", manufacturer=man)
        new_car = Car.objects.all()
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(new_car),
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")
