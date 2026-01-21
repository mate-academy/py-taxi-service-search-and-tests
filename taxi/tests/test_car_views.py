from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer


CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="TestManufacturer")
        Car.objects.create(model="Navara", manufacturer=manufacturer)
        Car.objects.create(model="Lanos", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_cars_by_model_returns_correct_results(self):
        manufacturer = Manufacturer.objects.create(name="TestManufacturer")
        Car.objects.create(model="Navara", manufacturer=manufacturer)
        Car.objects.create(model="Lanos", manufacturer=manufacturer)
        response = self.client.get(CAR_URL, {"model": "Navara"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Navara")
        self.assertNotContains(response, "Lanos")

    def test_search_car_by_model_no_match(self):
        manufacturer = Manufacturer.objects.create(name="TestManufacturer")
        Car.objects.create(model="Navara", manufacturer=manufacturer)
        Car.objects.create(model="Lanos", manufacturer=manufacturer)
        response = self.client.get(CAR_URL, {"model": "Camry"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Navara")
        self.assertNotContains(response, "Lanos")
        self.assertEqual(
            list(response.context["car_list"]),
            []
        )

    def test_search_car_without_query_returns_all(self):
        manufacturer = Manufacturer.objects.create(name="TestManufacturer")
        Car.objects.create(model="Navara", manufacturer=manufacturer)
        Car.objects.create(model="Lanos", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Navara")
        self.assertContains(response, "Lanos")
