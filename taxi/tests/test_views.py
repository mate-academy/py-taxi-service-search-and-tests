from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

manufacturer_url = reverse("taxi:manufacturer-list")
car_url = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(manufacturer_url)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test-user",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_all_manufacturers(self):
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="BMW")
        response = self.client.get(manufacturer_url)
        self.assertEqual(response.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(car_url)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test-user",
            password="test123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="Yaris",
            manufacturer=self.manufacturer
        )

    def test_view_accessible_for_authenticated_user(self):
        response = self.client.get(car_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
