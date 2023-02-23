from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )

    def test_car_list_login_required(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_car_detail_login_required(self):
        res = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": self.car.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_car_create_login_required(self):
        res = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_car_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:car-update", kwargs={"pk": self.car.id}
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_car_delete_login_required(self):
        res = self.client.get(reverse(
            "taxi:car-delete", kwargs={"pk": self.car.id}
        ))
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer
        )

        self.driver = get_user_model().objects.create_user(
            username="test_username",
            password="1234qwer"
        )
        self.client.force_login(self.driver)

    def test_retrieve_car(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_login_required(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.status_code, 200)

    def test_car_detail_login_required(self):
        res = self.client.get(reverse(
            "taxi:car-detail", kwargs={"pk": self.car.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_car_create_login_required(self):
        res = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(res.status_code, 200)

    def test_car_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:car-update", kwargs={"pk": self.car.id}
        ))
        self.assertEqual(res.status_code, 200)

    def test_car_delete_login_required(self):
        res = self.client.get(reverse(
            "taxi:car-delete", kwargs={"pk": self.car.id}
        ))
        self.assertEqual(res.status_code, 200)
