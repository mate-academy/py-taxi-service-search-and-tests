from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


class PublicCarTests(TestCase):

    def test_login_required_car_list_url(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_create_url(self):
        response = self.client.get(CAR_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_delete_url(self):
        self.manufacturer = Manufacturer.objects.create(name="test_man1", country="UK")
        self.car = Car.objects.create(model="test_car1", manufacturer_id=1)
        response = self.client.get(reverse("taxi:car-delete", kwargs={"pk": self.car.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_login_required_car_detail_url(self):
        self.manufacturer1 = Manufacturer.objects.create(name="test_man", country="UK")
        self.car1 = Car.objects.create(model="test_car", manufacturer_id=1)
        response = self.client.get(reverse("taxi:car-detail", kwargs={"pk": self.car1.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_login_required_car_update_url(self):
        self.manufacturer2 = Manufacturer.objects.create(name="test_man2", country="UK")
        self.car2 = Car.objects.create(model="test_car2", manufacturer_id=1)
        response = self.client.get(reverse("taxi:car-update", kwargs={"pk": self.car2.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))


class PrivateCarTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password1",
            license_number="ASD12345",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_m",
            country="UK_test",
        )

    def test_get_data_from_car_list(self):
        Car.objects.create(model="test1", manufacturer_id=self.manufacturer.pk)
        Car.objects.create(model="test2", manufacturer_id=self.manufacturer.pk)
        Car.objects.create(model="test3", manufacturer_id=self.manufacturer.pk)
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all().select_related("manufacturer")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
