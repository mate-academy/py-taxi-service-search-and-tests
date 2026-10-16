from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="testuser6",
            country="Germany"
        )
        Car.objects.create(
            model="BMW",
            manufacturer=manufacturer,
        )
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class CarSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser6",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_search_by_model_car(self):
        manufacturer = Manufacturer.objects.create(
            name="testuser6",
            country="Germany"
        )
        Car.objects.create(model="Ferrari", manufacturer=manufacturer)
        Car.objects.create(model="Tesla", manufacturer=manufacturer)
        response = self.client.get(reverse("taxi:car-list") + "?model=Ferrari")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ferrari")
        self.assertNotContains(response, "Tesla")
