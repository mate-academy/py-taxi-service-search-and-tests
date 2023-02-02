from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test1",
            password="Test12345"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Audi"
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="Audi"))
        )

    def test_search_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=Test"
        )

        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="Test"))
        )

    def test_search_car(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=taxi"
        )

        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="taxi"))
        )
