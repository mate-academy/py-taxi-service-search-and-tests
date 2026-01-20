from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicManufacturerTests(TestCase):
    def test_anonymous_access_false(self):
        response = self.client.get("/manufacturers/")
        self.assertNotEqual(response.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="USA"
        )
        Car.objects.create(
            model="test1",
            manufacturer=manufacturer
        )

        car1 = Car.objects.create(
            model="test2",
            manufacturer=manufacturer
        )

        user = get_user_model().objects.create_user(
            username="user",
            password="password"
        )
        car1.drivers.add(user)
        self.client.force_login(user)

    def test_car_list_exact(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

        car1 = Car.objects.get(pk=1)
        car2 = Car.objects.get(pk=2)

        self.assertEqual(list(response.context["car_list"]), [car1, car2])

    def test_car_list_search(self):
        response = self.client.get("/cars/?model=1")
        self.assertEqual(response.status_code, 200)

        car1 = Car.objects.get(pk=1)

        self.assertEqual(list(response.context["car_list"]), [car1])

    def test_car_delete_view_success_url(self):
        self.client.delete(
            reverse(
                "taxi:car-delete",
                kwargs={"pk": 1},
            ),
        )
        self.assertFalse(Car.objects.filter(pk=1))

    def test_car_toggle_assign(self):
        self.client.post(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": 2})
        )
        self.assertFalse(Car.objects.get(pk=1).drivers.all())

        self.client.post(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": 2})
        )
        car = Car.objects.get(pk=2)
        car.refresh_from_db()
        self.assertEqual(
            car.drivers.get(pk=1),
            get_user_model().objects.get(pk=1)
        )

    def test_index_num_visits(self):
        self.client.get(reverse(
            "taxi:index"
        ))

        self.assertEqual(self.client.session["num_visits"], 1)

        for _ in range(10):
            self.client.get(reverse(
                "taxi:index"
            ))

        self.assertEqual(self.client.session["num_visits"], 11)
