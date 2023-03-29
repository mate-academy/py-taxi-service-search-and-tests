from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class CarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Paul",
            license_number="KIA19754",
            first_name="Paul",
            last_name="Maslov",
            password="Platina07",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )

    def test_create_car(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Nautilus",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Car.objects.get(id=self.user.cars.first().id).model, "Nautilus"
        )

    def test_update_car(self):
        car = Car.objects.create(
            model="Nautilus",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": car.id}),
            {
                "pk": car.id,
                "model": "Navigator",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        Car.objects.get(id=car.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.get(id=car.id).model, "Navigator")

    def test_delete_car(self):
        car = Car.objects.create(
            model="Continental",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": car.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())
