from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer

Car_url = reverse("taxi:car-list")


class PublicCarListView(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(Car_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12234",
            license_number="TST00001"
        )
        self.client.force_login(self.user)
        manufacturer_car = Manufacturer.objects.create(
            name="VAG",
            country="German"
        )
        car = Car.objects.create(
            model="Audi",
            manufacturer=manufacturer_car,
        )
        car.drivers.add(self.user)

    def test_retrieve_car(self) -> None:
        response = self.client.get(Car_url)
        self.assertEqual(response.status_code, 200)
        car_all = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(car_all)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_by_car(self) -> None:
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Audi"}
        )
        self.assertContains(response, "Audi")
