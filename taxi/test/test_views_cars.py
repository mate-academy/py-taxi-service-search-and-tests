from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self) -> None:
        manufacturer = Manufacturer.objects.create(name="BMW")
        Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="X7", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

        car = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]),
                         list(car))

        self.assertTemplateUsed(response, "taxi/car_list.html")
