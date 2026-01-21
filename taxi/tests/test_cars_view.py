from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class CarListViewTest(TestCase):
    def setUp(self):
        self.User = get_user_model()

        self.user = self.User.objects.create_user(
            username="testuser",
            password="testpass"
        )
        manufacturer = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(model="Test model", manufacturer=manufacturer,)
        self.client.login(username="testuser", password="testpass")

    def test_car_view_url_exists_at_desired_location(self):
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)

    def test_car_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_lists_all_cars(self):
        response = self.client.get(reverse("taxi:car-list") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_car_search_functionality(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Test model"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["car_list"][0].model, "Test model")

    def test_invalid_car_search_form(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_get_queryset_with_car_model(self):
        response = self.client.get("/cars/?model=Test model")
        queryset = response.context["car_list"]

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].model, "Test model")

    def test_car_search_case_insensitive(self):
        response = self.client.get("/cars/?model=TEST MODEL")
        self.assertEqual(len(response.context["car_list"]), 1)
