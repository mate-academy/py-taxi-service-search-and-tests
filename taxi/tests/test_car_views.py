from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


CARS_URL = reverse("taxi:car-list")


def car_detail_url(pk: int) -> str:
    return reverse("taxi:car-detail", args=[pk])


class PrivateCarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_cars = 23

        cls.manufacturer_one = Manufacturer.objects.create(
            name="Test",
            country="Object",
        )

        cls.manufacturer_two = Manufacturer.objects.create(
            name="AnotherTest",
            country="Object",
        )

        for car_id in range(number_of_cars):
            Car.objects.create(
                model=f"Car {car_id}",
                manufacturer=cls.manufacturer_one,
            )

        cls.second_user = get_user_model().objects.create_user(
            username="secondtestsuser",
            password="test123",
            license_number="ABC12345",
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(CARS_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)
        self.assertEqual(list(response.context["car_list"]), list(cars)[:5])
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_cars_second_page(self):
        response = self.client.get(CARS_URL + "?page=5")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_retrieve_cars_search(self):
        response = self.client.get(CARS_URL + "?model=2")
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.filter(model__icontains=2)
        self.assertEqual(list(response.context["car_list"]), list(cars))

        response = self.client.get(CARS_URL + "?page=2&model=1")
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.filter(model__icontains=1)
        self.assertEqual(list(response.context["car_list"]), list(cars)[5:10])

    def test_retrieve_car_detail(self):
        response = self.client.get(car_detail_url(1))
        self.assertEqual(response.status_code, 200)
        car = Car.objects.get(pk=1)
        self.assertEqual(response.context["car"], car)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_create_car(self):
        form_data = {
            "model": "TestCar",
            "manufacturer": self.manufacturer_one.pk,
            "drivers": [self.second_user.pk, self.user.pk],
        }
        self.client.post(reverse("taxi:car-create"), data=form_data)

        new_car = Car.objects.get(model=form_data["model"])

        self.assertEqual(new_car.manufacturer.pk, form_data["manufacturer"])
        self.assertEqual(
            [driver.pk for driver in new_car.drivers.all()],
            form_data["drivers"],
        )

    def test_update_car(self):
        form_data = {
            "model": "NotTestCar",
            "manufacturer": self.manufacturer_two.pk,
            "drivers": [self.user.pk],
        }
        self.client.post(reverse("taxi:car-update", args=[1]), data=form_data)
        car = Car.objects.get(pk=1)

        self.assertEqual(car.model, form_data["model"])
        self.assertEqual(car.manufacturer.pk, form_data["manufacturer"])
        self.assertEqual(
            [driver.pk for driver in car.drivers.all()], form_data["drivers"]
        )

    def test_delete_car_get_request(self):
        response = self.client.get(
            reverse("taxi:car-delete", args=[1]),
            follow=True,
        )
        self.assertContains(response, "Delete car?")

    def test_delete_car_post_request(self):
        response = self.client.post(
            reverse("taxi:car-delete", args=[1]),
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("taxi:car-list"),
            status_code=302,
        )
