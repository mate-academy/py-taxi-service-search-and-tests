from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Car, Manufacturer


class PublicCarlistTest(TestCase):
    def test_manufacturer_list(self):
        res = self.client.get(
            reverse("taxi:car-list")
        )
        self.assertNotEqual(res.status_code, 200)

    def test_car_update_login_required(self):
        url = reverse("taxi:car-update", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_create_login_required(self):
        url = reverse("taxi:car-create")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_car_delete_login_required(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        Car.objects.create(
            model="test",
            manufacturer=self.manufacturer,
        )
        url = reverse(
            "taxi:car-delete",
            kwargs={"pk": self.manufacturer.id}
        )
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)


class PrivateAlllistTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.car1 = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.car2 = Car.objects.create(
            model="Another Model",
            manufacturer=self.manufacturer,
        )
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
        )
        self.client.force_login(self.driver)

    def test_car_list(self):
        form = CarSearchForm(data={"model": self.car1.model})
        respons = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(respons.status_code, 200)
        self.assertEqual(
            list(respons.context["car_list"]),
            list(Car.objects.all()))
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], self.car1.model)
        self.assertTemplateUsed(respons, "taxi/car_list.html")

    def test_search_functionality(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            data={"model": "test"}
        )
        self.assertContains(response, "Test Model")
        self.assertNotContains(response, "Another Model")

        response = self.client.get(
            reverse("taxi:car-list"),
            data={"model": "another"}
        )
        self.assertContains(response, "Another Model")
        self.assertNotContains(response, "Test Model")
