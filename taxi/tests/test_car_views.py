from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry"
        )
        self.car = Car.objects.create(
            model="TestModel",
            manufacturer=self.manufacturer
        )

    def test_retrieve_cars(self):
        Car.objects.create(model="Test1", manufacturer=self.manufacturer)
        Car.objects.create(model="Test2", manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_filters_queryset(self):
        model = "Test1"
        response = self.client.get(CAR_URL, {"model": model})

        self.assertEqual(response.status_code, 200)

        expected = Car.objects.filter(model__icontains=model)
        self.assertEqual(
            list(response.context["car_list"]),
            list(expected)
        )

    def test_search_empty_returns_all(self):
        response = self.client.get(CAR_URL, {"name": ""})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())
        )

    def test_create_car(self):
        manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry"
        )
        form_data = {
            "model": "TestModel",
            "manufacturer": manufacturer.id
        }
        self.client.post(reverse("taxi:car-create"), data=form_data)
        new_car = Car.objects.get(
            model=form_data["model"],
            manufacturer_id=form_data["manufacturer"]
        )

        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer_id, form_data["manufacturer"])

    def test_update_car(self):
        new_manufacturer = Manufacturer.objects.create(
            name="New",
            country="NewCountry"
        )
        form_data = {
            "model": "NewModel",
            "manufacturer": new_manufacturer.id
        }
        self.client.post(reverse(
            "taxi:car-update",
            args=[self.car.id]
        ), data=form_data)
        self.car.refresh_from_db()

        self.assertEqual(self.car.model, form_data["model"])
        self.assertEqual(self.car.manufacturer_id, form_data["manufacturer"])

    def test_confirm_delete_car(self):
        response = self.client.get(
            reverse(
                "taxi:car-delete",
                args=[self.car.id]
            ), follow=True
        )
        self.assertContains(response, "Delete car?")

    def test_delete_car(self):
        post_response = self.client.post(
            reverse(
                "taxi:car-delete",
                args=[self.car.id]
            ), follow=True
        )
        self.assertRedirects(post_response, reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())
