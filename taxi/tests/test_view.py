from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CARS_URLS = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_URLS)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="Test_driver",
            license_number="AAA11111",
            first_name="Some",
            last_name="Driver",
            password="driver-password",
        )
        self.client.force_login(self.driver)

    def test_login_required_with_user(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_name", country="Test_country"
        )
        Car.objects.create(
            model="Test-model",
            manufacturer=manufacturer,
        )

        response = self.client.get(CARS_URLS)
        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(car))
        self.assertTemplateUsed(response, "taxi/car_list.html")
