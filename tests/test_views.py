from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicFormatTests(TestCase):
    def test_manufacturer_login_required(self):
        result = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(result.status_code, 200)

    def test_driver_login_required(self):
        result = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(result.status_code, 200)

    def test_car_login_required(self):
        result = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(result.status_code, 200)


class PrivateFormatTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "12345678"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Ford")

        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturer = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_car(self):
        toyota = Manufacturer.objects.create(name="Toyota")
        ford = Manufacturer.objects.create(name="Ford")
        Car.objects.create(model="Toyota Camry", manufacturer=toyota)
        Car.objects.create(model="Ford Fiesta", manufacturer=ford)

        response = self.client.get(reverse("taxi:car-list"))
        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
