from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testtest123",
        )
        self.client.force_login(self.user)

    def test_authorized_user_can_access(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United Kingdom",
        )
        car1 = Car.objects.create(
            model="Test Car1",
            manufacturer=manufacturer,
        )
        car2 = Car.objects.create(
            model="Test Car2",
            manufacturer=manufacturer,
        )
        response = self.client.get(CAR_LIST_URL)
        queryset = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(queryset))
        self.assertContains(response, car1.model)
        self.assertContains(response, car2.model)
