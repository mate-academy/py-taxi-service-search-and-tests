from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer
from django.contrib.auth import get_user_model


class CarSearchTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="test", password="test1234", license_number="ABC12345"
        )
        self.client.login(username="test", password="test1234")
        manufacturer = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="Prius", manufacturer=manufacturer)
        Car.objects.create(model="Corolla Hybrid", manufacturer=manufacturer)
        self.client.force_login(user)

    def test_search_returns_matching_models(self):
        url = reverse("taxi:car-list")
        resp = self.client.get(url, {"model": "Corolla"})
        self.assertEqual(resp.status_code, 200)
        car_list = resp.context.get("car_list")
        self.assertIsNotNone(car_list)
        self.assertEqual(len(car_list), 2)
        models = [c.model for c in car_list]
        self.assertIn("Corolla", models)
        self.assertIn("Corolla Hybrid", models)

    def test_search_no_results(self):
        url = reverse("taxi:car-list")
        resp = self.client.get(url, {"model": "Nonexistent"})
        self.assertEqual(resp.status_code, 200)
        car_list = resp.context.get("car_list")
        self.assertEqual(len(car_list), 0)
