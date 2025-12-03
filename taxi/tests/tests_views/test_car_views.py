from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicCarTest(TestCase):
    def test_login_required_list_car(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test_username",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test_manufacturer",
            country="test_country"
        )

    def test_retrieve_car(self):
        Car.objects.create(
            model="Test_model_car1",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="Test_model_car2",
            manufacturer=self.manufacturer,
        )
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(res.context["car_list"]), list(cars))

    def test_search_car_by_model(self):
        Car.objects.create(
            model="Audi A8",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="BMW M5",
            manufacturer=self.manufacturer,
        )
        res = self.client.get(
            reverse("taxi:car-list"),
            data={"model": "au"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Audi A8")
        self.assertNotContains(res, "BMW M5")


class CarChangeTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test_manufacturer",
            country="Test_country"
        )
        self.car = Car.objects.create(
            model="Test_model",
            manufacturer=self.manufacturer
        )
        self.user = get_user_model().objects.create_user(
            username="Test_username",
            password="test123"
        )
        self.car.drivers.add(self.user)
        self.client.force_login(self.user)

    def test_car_update_redirect_to_success_url(self):
        res = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": self.car.pk}),
            data={
                "model": "Audi",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            }
        )
        self.assertRedirects(res, reverse("taxi:car-list"))

    def test_car_delete_redirect_to_success_url(self):
        res = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": self.car.pk})
        )
        self.assertRedirects(res, reverse("taxi:car-list"))
