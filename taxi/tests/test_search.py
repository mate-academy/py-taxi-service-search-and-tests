from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="new_user",
            license_number="ADM56984"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=BMW"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="BMW")),
        )

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?name=new_user"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="new_user")),
        )

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?model=Yaris"
        )
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="Yaris"))
        )
        