

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarViewsTests(TestCase):

    def test_login_required_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_car_detail(self):
        url = reverse("taxi:car-detail", args=[1])
        response = self.client.get(url)
        self.assertNotEquals(response.status_code, 200)


class PrivateCarViewsTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="test",
            password="password123",
            license_number="CBA54321"
        )
        self.user2 = get_user_model().objects.create_user(
            username="test2",
            password="password123",
            license_number="ABC12345"
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="test1",
            country="losos"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="test2",
            country="corop"
        )
        self.car1 = Car.objects.create(
            model="test1",
            manufacturer=self.manufacturer1,
        )
        self.car1.drivers.add(self.user2)
        self.car2 = Car.objects.create(
            model="test2",
            manufacturer=self.manufacturer2,
        )
        self.car2.drivers.add(self.user1)
        self.client.force_login(self.user1)

    def test_retrieve_cars_list(self):
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(response.context["car_list"]), list(cars))

    def test_retrieve_car_detail(self):
        url = reverse("taxi:car-detail", args=[self.car1.id])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["car"], self.car1)

    def test_add_driver_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car1.id])
        self.client.get(url)

        self.assertIn(self.user1, self.car1.drivers.all())

    def test_remove_driver_form_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car2.id])
        self.client.get(url)

        self.assertNotIn(self.user1, self.car2.drivers.all())

    def test_car_update_view(self):
        car_data = {
            "model": "test3",
            "manufacturer": self.manufacturer1.id,
            "drivers": [self.user1.id]
        }
        url = reverse("taxi:car-update", args=[self.car1.id])
        response = self.client.post(url, car_data)

        self.car1.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.car1.model, "test3")
        self.assertEqual(self.car1.manufacturer, self.manufacturer1)
        self.assertIn(self.user1, self.car1.drivers.all())

    def test_car_create_view(self):
        car_data = {
            "model": "test3",
            "manufacturer": self.manufacturer1.id,
            "drivers": [self.user1.id]
        }
        url = reverse("taxi:car-create")
        response = self.client.post(url, car_data)

        self.assertEqual(response.status_code, 302)

        created_car = Car.objects.last()

        self.assertEqual(created_car.model, car_data["model"])
        self.assertEqual(
            list(
                created_car.drivers.values_list("id", flat=True)
            ), car_data["drivers"]
        )

    def test_car_delete(self):
        url = reverse("taxi:car-delete", args=[self.car1.id])
        self.client.post(url)
        self.assertFalse(Car.objects.filter(id=self.car1.id).exists())
