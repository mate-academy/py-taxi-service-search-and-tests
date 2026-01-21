from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer

CARS_LIST_URL = reverse("taxi:car-list")
PAGINATION = 5


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="AAA54321",
            first_name="Admin",
            last_name="User",
            password="1qwerty2",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )

        for i in range(0, PAGINATION + 1):
            Car.objects.create(
                model=f"Test Model{i}",
                manufacturer=self.manufacturer,
            )

    def test_car_list(self):
        response = self.client.get(CARS_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars[:PAGINATION]),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail(self):
        response = self.client.get(reverse("taxi:car-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_car_list_response_with_correct_template(self):
        response = self.client.get(CARS_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail_response_with_correct_template(self):
        response = self.client.get(reverse("taxi:car-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_create_car(self):
        model = "Test Create"
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": model,
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Car.objects.get(id=self.user.cars.first().id).model, model
        )

    def test_update_car(self):
        model = "Test Update"
        updated_model = "Updated Model"
        car = Car.objects.create(
            model=model,
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": car.id}),
            {
                "pk": car.id,
                "model": updated_model,
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        Car.objects.get(id=car.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.get(id=car.id).model, updated_model)

    def test_delete_car(self):
        model = "Test Delete"
        car = Car.objects.create(
            model=model,
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())
