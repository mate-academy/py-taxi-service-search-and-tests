from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test", password="1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer_one = Manufacturer.objects.create(name="VW", country="German")
        manufacturer_two = Manufacturer.objects.create(name="BMW", country="German")
        Car.objects.create(model="golf", manufacturer=manufacturer_one)
        Car.objects.create(model="340i", manufacturer=manufacturer_two)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )

        self.assertTemplateUsed(response, "taxi/car_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="1234"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user123",
            "password2": "user123",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "ASD12345",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
