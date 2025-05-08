from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.forms import CarForm
from .test_index_view import PrivateIndexViewTests

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarViewsTests(TestCase):
    def test_access_not_logged_in_users(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarViewsTests(TestCase):
    def setUp(self):
        PrivateIndexViewTests.setUp(self)

    def test_car_list_view(self):
        res = self.client.get(CAR_LIST_URL)
        cars = Car.objects.select_related("manufacturer").all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]), list(cars)
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_car_detail_view(self):
        url = reverse("taxi:car-detail", args=[self.car.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["car"], self.car)
        self.assertTemplateUsed(res, "taxi/car_detail.html")

    def test_car_create_view_get(self):
        url = reverse("taxi:car-create")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["form"], CarForm)
        self.assertTemplateUsed(res, "taxi/car_form.html")

    def test_car_create_view_post(self):
        url = reverse("taxi:car-create")
        data = {
            "model": "New Test Model",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 302)
        self.assertTrue(Car.objects.filter(model="New Test Model").exists())

    def test_car_update_view_get(self):
        url = reverse("taxi:car-update", args=[self.car.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["form"], CarForm)
        self.assertTemplateUsed(res, "taxi/car_form.html")

    def test_car_update_view_post(self):
        url = reverse("taxi:car-update", args=[self.car.id])
        data = {
            "model": "Updated Test Model",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 302)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "Updated Test Model")

    def test_car_delete_view_get(self):
        url = reverse("taxi:car-delete", args=[self.car.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/car_confirm_delete.html")

    def test_car_delete_view_post(self):
        url = reverse("taxi:car-delete", args=[self.car.id])
        res = self.client.post(url)

        self.assertEqual(res.status_code, 302)
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())

    def test_car_search(self):
        Car.objects.create(
            model="Another Model",
            manufacturer=self.manufacturer
        )
        url = f"{CAR_LIST_URL}?model=Test"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["car_list"]), 1)
        self.assertEqual(res.context["car_list"][0], self.car)
