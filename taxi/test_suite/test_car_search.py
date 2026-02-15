from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer

User = get_user_model()


class CarSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        man1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        man2 = Manufacturer.objects.create(name="Ford", country="USA")
        Car.objects.create(model="Corolla", manufacturer=man1)
        Car.objects.create(model="Focus", manufacturer=man2)

    def test_search_by_model_returns_correct_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"search": "Cor"})
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

    def test_search_empty_returns_all_results(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertContains(response, "Corolla")
        self.assertContains(response, "Focus")

    def test_search_no_match_returns_empty(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"search": "BMW"})
        self.assertContains(response, "There are no cars in taxi")
