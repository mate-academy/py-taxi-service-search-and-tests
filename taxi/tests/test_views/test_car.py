from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer


CAR_URL = reverse("taxi:car-list")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="<PASSWORD>"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="testname",
            country="USA")

    def test_retrieve_cars(self):
        Car.objects.create(model="test", manufacturer=self.manufacturer)
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(res.context["car_list"]), list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")
        self.assertTrue(res.context["search_form"])
