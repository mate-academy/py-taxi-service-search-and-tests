from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestSearchers(TestCase):
    fixtures = ['taxi_service_db_data.json']

    def setUp(self) -> None:
        self.client.force_login(get_user_model().objects.get(id=1))

    def test_drivers_search_admin(self):
        response = self.client.get(reverse("taxi:driver-list") + "?username=admin")

        self.assertFalse("byers" in str(response.content))

    def test_cars_search_mx_30(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=mx-30")

        self.assertFalse("Mitsubishi" in str(response.content))

    def test_manufacturers_search_mazda(self):
        response = self.client.get(reverse("taxi:manufacturer-list") + "?name=mazda")

        self.assertFalse("BMW" in str(response.content))
