from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Car, Manufacturer


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer",
            country="TestCountry"
        )
        self.car = Car.objects.create(
            model="TestModel1",
            manufacturer=self.manufacturer
        )
        Car.objects.create(model="TestModel2", manufacturer=self.manufacturer)
        self.client = Client()

    def test_car_list_view_with_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestModel1")
        self.assertContains(response, "TestModel2")

    def test_car_list_view_without_login(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("taxi:car-list")
        )

    def test_get_queryset_with_model_parameter(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(
            "taxi:car-list"),
            {"model": "TestModel1"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestModel1")
        self.assertNotContains(response, "TestModel2")

    def test_get_queryset_without_model_parameter(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestModel1")
        self.assertContains(response, "TestModel2")

    def test_toggle_assign_to_car(self):
        self.client.force_login(self.user)

        self.assertNotIn(self.car, self.user.cars.all())

        response = self.client.get(reverse(
            "taxi:toggle-car-assign",
            args=[self.car.id]
        ))

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.car, self.user.cars.all())

        response = self.client.get(reverse(
            "taxi:toggle-car-assign",
            args=[self.car.id]
        ))

        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.car, self.user.cars.all())
