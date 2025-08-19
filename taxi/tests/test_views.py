from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

User = get_user_model()


class ManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(
            username="test",
            password="test123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)

    def test_manufacturer_create_view(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-create"
            ),
            {"name": "Ford", "country": "USA"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Ford").exists())


class DriverViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(
            username="test",
            password="test123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_driver_create_view(self):
        response = self.client.post(
            reverse(
                "taxi:driver-create"
            ),
            {
                "username": "test1",
                "password1": "test123Q123",
                "password2": "test123Q123",
                "first_name": "test_first",
                "last_name": "test_last",
                "license_number": "ABC12345"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="test1").exists())


class CarViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(
            username="test",
            password="test123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="Q5",
            manufacturer=self.manufacturer
        )

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

    def test_car_create_view(self):
        response = self.client.post(
            reverse(
                "taxi:car-create"
            ),
            {
                "model": "A6",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id]
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model="A6").exists())
