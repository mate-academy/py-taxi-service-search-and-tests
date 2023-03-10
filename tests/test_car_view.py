from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CARS_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_when_user_logout(self):
        response = self.client.get(CARS_URL)
        self.assertRedirects(response, f"{reverse('login')}?next=/cars/")


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        Car.objects.create(
            model="test_name",
            manufacturer=Manufacturer.objects.create(
                name="Test name", country="Test country"
            ),
        )
        Car.objects.create(
            model="test_name 2",
            manufacturer=Manufacturer.objects.create(
                name="Test name 2", country="Test country 2"
            ),
        )

        response = self.client.get(CARS_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_on_cars_list_page(self):
        Car.objects.create(
            model="test_123123123",
            manufacturer=Manufacturer.objects.create(
                name="Test name 2", country="Test country 2"
            ),
        )

        response = self.client.get(
            reverse("taxi:car-list"), {"model": "test_123123123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="test_123123123")),
        )
