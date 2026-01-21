from django.contrib.auth import get_user_model

from django.urls import reverse
from django.test import TestCase

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self) -> None:
        test_response = self.client.get(CAR_URL)
        self.assertNotEqual(test_response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="country"
        )
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpassword"
        )
        self.client.force_login(self.driver)

    def test_retrieve_car_list(self):
        car1 = Car.objects.create(
            model="car1",
            manufacturer=self.manufacturer
        )
        car1.drivers.add(self.driver)
        car2 = Car.objects.create(
            model="car2",
            manufacturer=self.manufacturer
        )
        car2.drivers.add(self.driver)
        test_response = self.client.get(CAR_URL)
        self.assertEqual(test_response.status_code, 200)
        all_cars = Car.objects.all()
        self.assertEqual(all_cars.count(), 2)
        self.assertTemplateUsed(test_response, "taxi/car_list.html")
