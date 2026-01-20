from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_list_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEquals(response.status_code, 200)


class PrivateCarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="country",
        )

        car_count = 5

        for i in range(car_count):
            Car.objects.create(
                model=f"model{i}",
                manufacturer=manufacturer,
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(
            list(response.context["car_list"]),
            list(cars)
        )

    def test_car_list_search_by_model(self):
        search_value = "3"
        response = self.client.get(CAR_LIST_URL, {"model": search_value})
        cars = Car.objects.filter(model__icontains=search_value)

        self.assertQuerysetEqual(
            list(response.context["car_list"]),
            list(cars)
        )
