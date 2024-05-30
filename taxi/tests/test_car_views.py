from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer

car_url = reverse("taxi:car-list")


class PublicCarTest(TestCase):

    def test_login_required(self):
        res = self.client.get(car_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarListViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Audi", manufacturer=manufacturer)
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        response = self.client.get(car_url)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
