from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class TestSearch(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Ford"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="Ford")),
        )

    def test_search_drivers_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?name=test_user"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="test_user")),
        )

    def test_search_cars_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?name=Continental"
        )
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="Continental")),
        )
