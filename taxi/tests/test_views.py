from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver

User = get_user_model()


class PublicViewsTest(TestCase):

    def test_login_required_for_index(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer
        )

    def test_index_view_status_code(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_drivers", response.context)

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "Audi"}
        )

        self.assertContains(response, "Audi")
        self.assertNotContains(response, "BMW")

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")

    def test_car_search_by_model(self):
        Car.objects.create(
            model="A6",
            manufacturer=self.manufacturer
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "A6"}
        )

        self.assertContains(response, "A6")
        self.assertNotContains(response, "X5")

    def test_car_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_driver_search(self):
        Driver.objects.create_user(
            username="another_driver",
            password="12345",
            license_number="BBB12345",
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "another"},
        )

        self.assertEqual(len(response.context["driver_list"]), 1)
        self.assertEqual(
            response.context["driver_list"][0].username,
            "another_driver",
        )

    def test_toggle_assign_car(self):
        self.assertNotIn(self.car, self.user.cars.all())

        self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )

        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())

        self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )

        self.user.refresh_from_db()
        self.assertNotIn(self.car, self.user.cars.all())
