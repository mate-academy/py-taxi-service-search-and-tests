from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicCarTest(TestCase):
    cars_urls = reverse("taxi:car-list")

    def test_login_required(self) -> None:
        response = self.client.get(self.cars_urls)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.cars_urls = reverse("taxi:car-list")
        self.driver = get_user_model().objects.create_user(
            username="Test_driver",
            license_number="AAA11111",
            first_name="Some",
            last_name="Driver",
            password="driver-password",
        )
        self.client.force_login(self.driver)

    def test_login_required_with_user(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test_name", country="Test_country"
        )
        Car.objects.create(
            model="Test-model",
            manufacturer=manufacturer,
        )

        response = self.client.get(self.cars_urls)
        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(car))
        self.assertTemplateUsed(response, "taxi/car_list.html")
