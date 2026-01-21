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
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.create_cars()

    def create_cars(self):
        manufacturer1 = Manufacturer.objects.create(name="Toyota",
                                                    country="Japan")
        manufacturer2 = Manufacturer.objects.create(name="Honda",
                                                    country="Japan")
        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="Civic",
            manufacturer=manufacturer2,
        )
        self.car3 = Car.objects.create(
            model="Accord",
            manufacturer=manufacturer2,
        )

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(list(response.context["car_list"]), list(cars))

    def test_search_cars(self):
        search_term = "Civic"
        response = self.client.get(CAR_URL, {"model": search_term})
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.filter(model__icontains=search_term)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(list(response.context["car_list"]), list(cars))
