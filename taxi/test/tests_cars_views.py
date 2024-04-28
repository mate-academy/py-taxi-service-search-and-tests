from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer


class PrivateManufactureViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        Car.objects.create(
            model="Fiat",
            manufacturer=Manufacturer.objects.create(
                name="wethout_char",
            ))
        Car.objects.create(
            model="Fuat",
            manufacturer=Manufacturer.objects.create(
                name="with_char_i",
            ))
        Car.objects.create(
            model="Fiat1",
            manufacturer=Manufacturer.objects.create(
                name="with_char_i1",
            ))
        Car.objects.create(
            model="Fuat1",
            manufacturer=Manufacturer.objects.create(
                name="wethout_char1",
            ))

    def test_cars_list_search(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"car_model": "i",
                                    "car_manufacture": "i"})
        self.assertEqual(
            list(response.context_data["car_list"]),
            list(Car.objects.filter(
                model__icontains="i"
            ).filter(manufacturer__name__icontains="i"))
        )

    def test_car_create_get_succses_redirect(self):
        url = reverse("taxi:car-create")
        response = self.client.post(
            path=url,
            data={"model": "Fuat12", "manufacturer": 1}
        )
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_car_update_get_succses_redirect(self):
        url = reverse("taxi:car-update", args=["1"])
        response = self.client.post(
            path=url,
            data={"model": "Fuat123", "manufacturer": 1, "drivers": 1}
        )
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_car_delete_get_succses_redirect(self):
        url = reverse("taxi:car-delete", args=["1"])
        response = self.client.post(path=url)
        self.assertRedirects(response, reverse("taxi:car-list"))
