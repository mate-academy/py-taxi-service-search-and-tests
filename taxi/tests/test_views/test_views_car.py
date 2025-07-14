from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")
pagination_num = 5


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def create_cars_to_test(self):
        Manufacturer.objects.create(
            name="BMV",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="FIAT",
            country="Italy",
        )
        Car.objects.create(
            model="Convertible",
            manufacturer=Manufacturer.objects.get(name="BMV"),
        )
        Car.objects.create(
            model="500",
            manufacturer=Manufacturer.objects.get(name="FIAT"),
        )

        for num in range(10):
            manufacturer = Manufacturer.objects.create(
                name=f"TestManufacturer{num}",
                country=f"TestCountry{num}",
            )
            Car.objects.create(
                model=f"TestCar{num}",
                manufacturer=manufacturer,
            )

    def test_retrieve_cars(self):
        self.create_cars_to_test()

        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars[:pagination_num])
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
        search_response = self.client.get(f"{CAR_URL}?model=C")
        self.assertContains(search_response, "Convertible")
        self.assertNotContains(search_response, "500")

    def test_cars_pagination(self):
        self.create_cars_to_test()
        response = self.client.get(CAR_URL)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_car_detail(self):
        self.create_cars_to_test()
        car = Car.objects.get(id=1)
        response = self.client.get(reverse("taxi:car-detail", args=[car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertEqual(response.context["car"], car)
        self.assertContains(response, f"{car.model}")
        self.assertContains(response, f"{car.manufacturer.name}")
        self.assertContains(response, f"{car.manufacturer.country}")
        response = self.client.get(reverse("taxi:car-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)
