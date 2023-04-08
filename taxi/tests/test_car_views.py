from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


CARS_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CARS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        cls.driver = Driver.objects.create(
            username="driver1",
            first_name="John",
            last_name="Doe",
            license_number="123456",
        )
        cls.car = Car.objects.create(
            model="Model S",
            manufacturer=cls.manufacturer,
        )

    def setUp(self):
        self.client.login(username="testuser", password="testpass")

    def test_car_list_view(self):
        response = self.client.get(CARS_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(cars), list(response.context["car_list"]))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_with_search(self):
        response = self.client.get(CARS_URL, {"model": "Model S"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model S")

    def test_car_create_view(self):
        form_data = {
            "model": "Model X",
            "manufacturer": self.manufacturer.id,
            "drivers": self.driver.id,
        }
        response = self.client.post(
            reverse("taxi:car-create"),
            data=form_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.count(), 2)

    def test_car_delete_view(self):
        response = self.client.post(
            reverse("taxi:car-delete", kwargs={"pk": self.car.pk}),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.count(), 0)
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())
