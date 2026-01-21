from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarFormatTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarFormatTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Concern",
            country="Germany"
        )
        self.first_car = Car.objects.create(
            model="BMW",
            manufacturer=self.manufacturer
        )
        self.second_car = Car.objects.create(
            model="Mercedes",
            manufacturer=self.manufacturer
        )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.client.force_login(self.user)
        self.first_car.drivers.add(self.user)
        self.second_car.drivers.add(self.user)

    def test_car(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        # print(f"Context {response.context}")
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car_by_model(self):
        response = self.client.get(CAR_URL, data={"param": "BM"})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Mercedes")

    def test_search_car_model_not_found(self):
        response = self.client.get(CAR_URL, data={"param": "GG"})
        self.assertEqual(response.status_code, 200)

    def test_searching_car_find_all_if_name_empty(self):
        response = self.client.get(CAR_URL, {"username": ""})
        self.assertContains(response, "BMW")
        self.assertContains(response, "Mercedes")


class CarChangeTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Bavaria",
            country="Germany"
        )

        self.car = Car.objects.create(
            model="BMW 1",
            manufacturer=self.manufacturer
        )
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.car.drivers.add(self.user)
        self.client.force_login(self.user)

    def test_car_update_redirects_to_success_url(self):
        response = self.client.post(
            reverse(
                "taxi:car-update",
                kwargs={"pk": self.car.pk}
            ), data={"model": "test",
                     "manufacturer": self.manufacturer.id,
                     "drivers": [self.user.id], }
        )
        self.assertRedirects(response, CAR_URL)

    def test_car_successful_deletion_redirects_to_success_url(self):
        response = self.client.post(
            reverse(
                "taxi:car-delete",
                kwargs={"pk": self.car.pk}
            )
        )
        self.assertRedirects(response, CAR_URL)
