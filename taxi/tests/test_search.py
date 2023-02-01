from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class ModelsTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)

        Manufacturer.objects.create(name="Renault")
        Manufacturer.objects.create(name="BMW")

        self.user = get_user_model().objects.create_user(
            username="Taras",
            password="Shevchenko123456",
            license_number="ADS124852"
        )

        toyota = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(
            model="Toyota Yaris",
            manufacturer=toyota,
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(MANUFACTURER_URL, data={"name": "b"})
        queryset = Manufacturer.objects.filter(name__icontains="b")

        self.assertEqual(response.context["manufacturer_list"][0], queryset[0])

    def test_car_search_by_model(self):

        response = self.client.get(CAR_URL, data={"model": "toy"})
        queryset = Car.objects.filter(model__icontains="toy")

        self.assertEqual(response.context["car_list"][0], queryset[0])

    def test_driver_search_by_username(self):

        response = self.client.get(DRIVER_URL, data={"username": "ta"})
        queryset = get_user_model().objects.filter(username__icontains="ta")

        self.assertEqual(
            response.context["driver_list"][0].username, queryset[0].username
        )
