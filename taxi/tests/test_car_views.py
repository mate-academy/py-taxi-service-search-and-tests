from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )

    def test_page_available_for_logged_in_user(self):
        self.client.force_login(self.user)
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_page_uses_correct_template(self):
        self.client.force_login(self.user)
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_login_required(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_car_search_by_model(self):
        self.client.force_login(self.user)
        manufacturer_bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        manufacturer_skoda = Manufacturer.objects.create(
            name="Skoda",
            country="Czechia",
        )
        bmw = Car.objects.create(model="BMW X5", manufacturer=manufacturer_bmw)
        skoda = Car.objects.create(
            model="SKODA OCTAVIA A5",
            manufacturer=manufacturer_skoda,
        )
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "BMW X5"})
        self.assertContains(response, bmw.model)
        self.assertNotContains(response, skoda.model)
