from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car


class SearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Mustang",
            manufacturer=self.manufacturer2
        )

    def test_search_form_in_manufacturer_list_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?search_text=Toyota"
        )
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_search_form_in_car_list_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("taxi:car-list") + "?search_text=Corolla"
        )
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Mustang")
