from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})


class PublicCarTests(TestCase):
    def test_login_required_car_list(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/cars/")

    def test_login_required_car_detail(self):
        response = self.client.get(CAR_DETAIL_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/cars/1/")


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123456",
            first_name="test",
            last_name="test"
        )
        self.client.force_login(self.user)
        manufacturer1 = Manufacturer.objects.create(
            name="test1",
            country="test1"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="test2",
            country="test2"
        )
        Car.objects.create(model="test1", manufacturer=manufacturer1)
        Car.objects.create(model="test2", manufacturer=manufacturer2)

    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)

    def test_retrieve_car_detail(self):
        response = self.client.get(CAR_DETAIL_URL)

        self.assertEqual(response.status_code, 200)
