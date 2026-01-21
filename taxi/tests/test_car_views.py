from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class CarViewsTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            email="<EMAIL>",
            password="<PASSWORD>",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Car.objects.create(
            model="Range Rover",
            manufacturer=Manufacturer.objects.create(
                name="Land Rover",
                country="United Kingdom",
            ),
        )
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

        car = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )

    def test_manufacturer_template_name(self):
        response = self.client.get(CAR_URL)
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )

    def test_car_search(self):
        Car.objects.create(
            model="Range Rover",
            manufacturer=Manufacturer.objects.create(
                name="Land Rover",
                country="United Kingdom",
            ),
        )
        Car.objects.create(
            model="SLK-Class",
            manufacturer=Manufacturer.objects.create(
                name="Mercedes-Benz",
                country="Germany",
            ),
        )
        car = Car.objects.filter(model="SLK-Class")
        response = self.client.get(f"{CAR_URL}?model=SLK")
        self.assertEqual(list(response.context["car_list"]), list(car))
