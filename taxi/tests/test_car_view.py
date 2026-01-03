from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

CAR_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="pass123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_retrieve_cars(self):
        Car.objects.create(model="Camry", manufacturer=self.manufacturer)
        Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_create_car(self):
        driver = Driver.objects.create_user(
            username="TestUsername",
            password="TestPassword123@?",
            first_name="TestFirstName",
            last_name="TestLastName",
            license_number="ABC12345"
        )
        payload = {
            "model": "Prius",
            "manufacturer": self.manufacturer.id,
            "drivers": [driver.id]
        }
        self.client.post(CAR_CREATE_URL, payload)
        self.assertTrue(
            Car.objects.filter(
                model=payload["model"],
                manufacturer=self.manufacturer,
            ).exists()
        )
