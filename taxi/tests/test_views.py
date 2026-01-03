from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

URL = reverse("taxi:car-list")


class PublicLoginRequireTest(TestCase):
    def test_login_required(self):
        response = self.client.get(URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateLoginRequireTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )

        car = Car.objects.create(
            model="test_first_model",
            manufacturer=manufacturer,
        )
        car.drivers.set([self.user])

        car = Car.objects.create(
            model="test_second_model",
            manufacturer=manufacturer,
        )
        car.drivers.set([self.user])

        response = self.client.get(URL)
        self.assertEquals(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEquals(list(response.context["car_list"]), list(cars))

        self.assertTemplateUsed(response, "taxi/car_list.html")
