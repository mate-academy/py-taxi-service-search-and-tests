from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CARS_LIST_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test manufacturer"
        )
        self.car = Car.objects.create(
            model="test car",
            manufacturer=self.manufacturer
        )

    def test_car_list_login_required(self):
        res = self.client.get(CARS_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_car_detail_login_required(self):
        res = self.client.get(reverse(
            "taxi:car-detail", args=[self.car.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_car_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:car-update", args=[self.car.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_car_delete_login_required(self):
        res = self.client.get(reverse(
            "taxi:car-delete", args=[self.car.id]
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test manufacturer"
        )
        number_of_cars = 5
        for num in range(number_of_cars):
            Car.objects.create(
                model=f"car{num}",
                manufacturer=self.manufacturer
            )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        response = self.client.get(CARS_LIST_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["car_list"], cars)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_by_model_in_car_list(self):
        search_word = "car2"
        response = self.client.get(f"{CARS_LIST_URL}?field={search_word}")
        searched_query = Car.objects.filter(model__icontains=search_word)
        self.assertQuerysetEqual(response.context["car_list"], searched_query)
