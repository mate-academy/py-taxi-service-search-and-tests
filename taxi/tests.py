from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user",
            password="password123",
            license_number="AAA11111"
        )
        self.client.login(username="test.user", password="password123")

        self.manufacturer1 = (Manufacturer.objects
                              .create(name="Toyota", country="Japan"))
        self.manufacturer2 = (Manufacturer
                              .objects.create(name="Tesla", country="USA"))

    def test_retrieve_manufacturers(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Toyota")
        self.assertContains(res, "Tesla")

    def test_search_manufacturer_by_name(self):
        res = self.client.get(reverse("taxi:manufacturer-list"),
                              data={"name": "toy"})
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "Tesla")


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test.user.car",
            password="password123",
            license_number="BBB22222"
        )
        self.client.login(username="test.user.car", password="password123")

        self.manufacturer = (Manufacturer.objects
                             .create(name="Ford", country="USA"))

        self.car1 = (Car.objects
                     .create(model="Focus", manufacturer=self.manufacturer))
        self.car2 = (Car.objects
                     .create(model="Mustang", manufacturer=self.manufacturer))

    def test_retrieve_cars(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Focus")
        self.assertContains(res, "Mustang")

    def test_search_car_by_model(self):
        res = self.client.get(reverse("taxi:car-list"), data={"model": "foc"})
        self.assertContains(res, "Focus")
        self.assertNotContains(res, "Mustang")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="current.driver",
            password="password123",
            license_number="CCC33333"
        )
        self.client.login(username="current.driver", password="password123")

        self.driver1 = get_user_model().objects.create_user(
            username="jack.daniels",
            password="password123",
            license_number="DDD44444"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="john.doe",
            password="password123",
            license_number="EEE55555"
        )

    def test_retrieve_drivers(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "jack.daniels")
        self.assertContains(res, "john.doe")

    def test_search_driver_by_username(self):
        res = self.client.get(reverse("taxi:driver-list"),
                              data={"username": "jack"})
        self.assertContains(res, "jack.daniels")
        self.assertNotContains(res, "john.doe")
