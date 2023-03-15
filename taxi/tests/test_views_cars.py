from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", args=[1])


class PublicCarTest(TestCase):
    def test_car_list_login_required(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_car_detail_login_required(self):
        res = self.client.get(CAR_DETAIL_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="driver1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        manufacturer1 = Manufacturer.objects.create(
            name="AAA",
            country="Country_1"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="BBB",
            country="Country_2"
        )
        Car.objects.create(model="Test1", manufacturer=manufacturer1)
        Car.objects.create(model="Test2", manufacturer=manufacturer2)

        res = self.client.get(CAR_LIST_URL)

        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(
            response=res,
            template_name="taxi/car_list.html"
        )

    def test_retrieve_car_detail(self):
        manufacturer1 = Manufacturer.objects.create(
            name="AAA",
            country="Country_1"
        )
        Car.objects.create(model="Test1", manufacturer=manufacturer1)

        res = self.client.get(CAR_DETAIL_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            response=res,
            template_name="taxi/car_detail.html"
        )
